import time

import pandas as pd
from dask import dataframe as dd


def read_csv_as_dask_dataframe(path):

    dask_dataframe = dd.read_csv(path, dtype=object)

    return dask_dataframe


def optimize_types_in_dask_dataframe(dask_dataframe):

    to_category_cols = ["title", "url", "artist", "region", "trend", "chart"]
    to_datetime64_cols = ["date"]
    to_int32_cols = ["rank"]

    for col in to_category_cols:
        dask_dataframe[col] = dask_dataframe[col].astype("category")

    for col in to_int32_cols:
        dask_dataframe[col] = dask_dataframe[col].astype("int32")

    for col in to_datetime64_cols:
        dask_dataframe[col] = dask_dataframe[col].astype("datetime64")

    dask_dataframe = dask_dataframe.drop("trend", axis=1)
    dask_dataframe = dask_dataframe.drop("url", axis=1)

    return dask_dataframe


def dask_to_pandas_dataframe(dask_dataframe):

    dataframe = dask_dataframe.compute()

    return dataframe


def optimize_dataframe(dataframe):

    dataframe["streams"].fillna(value=0, inplace=True)
    dataframe["streams"] = dataframe["streams"].astype("int32")
    dataframe.dropna(inplace=True)

    return dataframe


def optimization(path):

    dask_dataframe = read_csv_as_dask_dataframe(path)
    dask_dataframe = optimize_types_in_dask_dataframe(dask_dataframe)
    dataframe = dask_to_pandas_dataframe(dask_dataframe)
    dataframe = optimize_dataframe(dataframe)

    return dataframe


def creating_cleaned_dataframe(path):

    dataframe = optimization(path)

    return dataframe[0:5].to_csv("test_csv.csv", index=False)


creating_cleaned_dataframe(
    "/home/damian/spotify_data_visualization/source/spotify_data/data/spotify_charts.csv"
)
