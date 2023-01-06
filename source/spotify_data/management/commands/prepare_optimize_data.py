import logging
import logging.config
from pathlib import Path

import pandas as pd
from dask import dataframe as dd
from django.core.management.base import BaseCommand
from spotify_data.constants import (DASK_COLUMNS_TO_CATEGORY,
                                    DASK_COLUMNS_TO_DATETIME64,
                                    DASK_COLUMNS_TO_DROP,
                                    DASK_COLUMNS_TO_INT32,
                                    PANDAS_COLUMNS_TO_CATEGORY,
                                    PANDAS_COLUMNS_TO_INT32,
                                    PANDAS_COLUMNS_TO_TRIM_DATA,
                                    UNOPTIMIZABLE_COLUMNS)
from spotify_data.exceptions import (NoFilesException,
                                     NotExistingDirectoryException,
                                     WrongFileTypeException)
from spotify_data.models import SpotifyData

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "path", type=str, help="Directory path with input csv files"
        )

        parser.add_argument(
            "output", type=str, help="Directory path with output csv files"
        )

        parser.add_argument("filename", type=str, help="New file name")

    def handle(self, path, output, filename, *args, **options):

        logging.info(f"Preparing data from {path}...")
        dask_dataframe = self.read_csv_dask_dataframe(path)
        dask_dataframe = self.remove_irrelevant_columns(dask_dataframe)
        dask_dataframe = self.optimize_types_in_dask(dask_dataframe)
        dataframe = self.dask_to_pandas(dask_dataframe)
        dataframe = self.fill_na(dataframe)
        dataframe = self.optimize_types_in_pandas(dataframe)
        dataframe = self.drop_na(dataframe)
        dataframe = self.trim_data(dataframe)
        dataframe = self.optimize_types_after_trim(dataframe)
        self.save_file_as_csv(dataframe, path, output, filename)

    def read_csv_dask_dataframe(self, path):
        # Load a csv into a Dask Dataframe (due to it's size) and return it

        try:
            dask_dataframe = dd.read_csv(path, dtype=object)
        except FileNotFoundError as e:
            raise NoFilesException("No such file or directory") from e

        return dask_dataframe

    def remove_irrelevant_columns(self, dask_dataframe):

        for column in DASK_COLUMNS_TO_DROP:
            dask_dataframe = dask_dataframe.drop(column, axis=1)

        return dask_dataframe

    def optimize_types_in_dask(self, dask_dataframe):

        for column in UNOPTIMIZABLE_COLUMNS:
            if column in DASK_COLUMNS_TO_CATEGORY:
                dask_dataframe[column] = dask_dataframe[column].astype("category")
            elif column in DASK_COLUMNS_TO_INT32:
                dask_dataframe[column] = dask_dataframe[column].astype("int32")
            elif column in DASK_COLUMNS_TO_DATETIME64:
                dask_dataframe[column] = dask_dataframe[column].astype("datetime64")
            else:
                pass

        return dask_dataframe

    def dask_to_pandas(self, dask_dataframe):

        dataframe = dask_dataframe.compute()

        return dataframe

    def fill_na(self, dataframe):

        for column in PANDAS_COLUMNS_TO_INT32:
            dataframe[column].fillna(value=0, inplace=True)

        return dataframe

    def optimize_types_in_pandas(self, dataframe):

        for column in PANDAS_COLUMNS_TO_INT32:
            dataframe[column] = dataframe[column].astype("int32")

        return dataframe

    def drop_na(self, dataframe):

        dataframe.dropna(inplace=True)

        return dataframe

    def trim_data(self, dataframe):

        for column in PANDAS_COLUMNS_TO_TRIM_DATA:
            dataframe[column] = dataframe[column].map(
                lambda x: x[:57] + "..." if len(x) > 60 else x
            )

        return dataframe

    def optimize_types_after_trim(self, dataframe):

        for column in PANDAS_COLUMNS_TO_CATEGORY:
            if column in PANDAS_COLUMNS_TO_CATEGORY:
                dataframe[column] = dataframe[column].astype("category")

        return dataframe

    def save_file_as_csv(self, dataframe, path, output, filename):
        try:
            dataframe[0:300000].to_csv(f"{Path(output)}/{filename}", sep=",", index=False)
            logging.info(
                f"Prepared new csv file: {path} - {filename} for {len(dataframe)} spotify_data \n"
            )
            logging.info(dataframe.info(memory_usage="deep"))
        except OSError as e:
            raise NotExistingDirectoryException(
                "Cannot save file into a non-existent directory"
            )
