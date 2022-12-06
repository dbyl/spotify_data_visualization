from pathlib import Path

import pandas as pd
from dask import dataframe as dd
import pytest
import numpy as np

from spotify_data.exceptions import NoFilesException
from spotify_data.management.commands.prepare_optimize_data import Command

from spotify_data.constants import (DASK_COLUMNS_TO_DROP,    
                                    UNOPTIMIZABLE_COLUMNS,
                                    DASK_COLUMNS_TO_CATEGORY,
                                    DASK_COLUMNS_TO_DATETIME64,
                                    DASK_COLUMNS_TO_INT32,
                                    PANDAS_COLUMNS_TO_INT32)

@pytest.fixture
def command():
    return Command()


def test_read_csv_with_proper_amount_of_columns_and_rows(command):
    path = Path('fixtures/unoptimized_data_sample.csv')
    dd = command.read_csv_dask_dataframe(path)

    assert len(dd.columns) == 9
    assert len(dd.index) == 50

def test_removing_tables(command):
    path = Path('fixtures/unoptimized_data_sample.csv')
    dd = command.read_csv_dask_dataframe(path)
    dd = command.remove_irrelevant_columns(dd)

    assert len(dd.columns) == 7

    for column in DASK_COLUMNS_TO_DROP:
        assert column not in dd.columns


def test_dask_data_optimization_types(command):
    path = Path('fixtures/unoptimized_data_sample.csv')
    dd = command.read_csv_dask_dataframe(path)
    dd = command.optimize_types_in_dask(dd)

    for column in DASK_COLUMNS_TO_CATEGORY:
        assert dd[column].dtype == "category"
    for column in DASK_COLUMNS_TO_DATETIME64:
        assert dd[column].dtype == "datetime64[ns]"
    for column in DASK_COLUMNS_TO_INT32:
        assert dd[column].dtype == "int32"


def test_dask_to_pandas(command):
    path = Path('fixtures/unoptimized_data_sample.csv')
    dd = command.read_csv_dask_dataframe(path)
    df = command.dask_to_pandas(dd)
    
    assert type(df) is pd.DataFrame


def test_fillna_streams(command):
    path = Path('fixtures/unoptimized_data_sample.csv')
    dd = command.read_csv_dask_dataframe(path)
    df = command.dask_to_pandas(dd)

    assert np.isnan(df.iloc[5,8])
    assert np.isnan(df.iloc[12,8])

    df = command.fill_na(df)
    
    assert df.iloc[5,8] == 0
    assert df.iloc[12,8] == 0    


def test_pandas_data_optimization_types(command):
    path = Path('fixtures/unoptimized_data_sample.csv')
    dd = command.read_csv_dask_dataframe(path)
    dd = command.optimize_types_in_dask(dd)
    df = command.dask_to_pandas(dd)
    df = command.fill_na(df)
    df = command.optimize_types_in_pandas(df)

    for column in PANDAS_COLUMNS_TO_INT32:
        assert df[column].dtype == "int32"


def test_drop_na(command):
    path = Path('fixtures/unoptimized_data_sample.csv')
    dd = command.read_csv_dask_dataframe(path)
    dd = command.optimize_types_in_dask(dd)
    df = command.dask_to_pandas(dd)
    df = command.fill_na(df)
    df = command.optimize_types_in_pandas(df)

    assert len(df.index) == 50

    df = command.drop_na(df)

    assert len(df.index) == 47

def test_save_correct_file(path, command):
    pass