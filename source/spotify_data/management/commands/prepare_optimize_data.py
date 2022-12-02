import logging
import logging.config
from pathlib import Path
from dask import dataframe as dd
import pandas as pd

from django.core.management.base import BaseCommand

from spotify_data.constants import (DASK_COLUMNS_TO_DROP,    
                                    UNOPTIMIZABLE_COLUMNS,
                                    DASK_COLUMNS_TO_CATEGORY,
                                    DASK_COLUMNS_TO_DATETIME64,
                                    DASK_COLUMNS_TO_INT32,
                                    PANDAS_COLUMNS_TO_INT32)
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

    def handle(self, path, output, *args, **options):

        logging.info(f"Preparing data from {path}...")
        dask_dataframe = self.read_csv_dask_dataframe(path)
        dask_dataframe = self.remove_irrelevant_columns(dask_dataframe)
        dask_dataframe = self.optimize_types_in_dask(dask_dataframe)
        dataframe = self.dask_to_pandas(dask_dataframe)
        dataframe = self.fill_na(dataframe)
        dataframe = self.optimize_types_in_pandas(dataframe)
        dataframe = self.drop_na(dataframe)
        self.save_file_as_csv(dataframe, path, output)
        print(dataframe.info(memory_usage='deep'))


    def read_csv_dask_dataframe(self, path):
        # Load a csv into a Dask Dataframe (due to it's size) and return it
        dask_dataframe = dd.read_csv(path, dtype=object)

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

    def save_file_as_csv(self, dataframe, path, output):
        try:
            dataframe[0:100].to_csv(f"/home/damian/spotify_data_visualization/source/spotify_data/data/cleaned_data_sample.csv", sep=",")
            logging.info(
                f"Prepared new csv file: {path} for {len(dataframe)} spotify_data \n"
            )
        except OSError as e:
            raise NotExistingDirectoryException(
                "Cannot save file into a non-existent directory"
            )


    
