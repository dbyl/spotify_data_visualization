from pathlib import Path

import pandas as pd
from dask import dataframe as dd
import pytest
import numpy as np

from spotify_data.exceptions import NoFilesException, NotExistingDirectoryException
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
    path = Path('spotify_data/tests/fixtures/unoptimized_data_sample.csv')
    dd = command.read_csv_dask_dataframe(path)

    assert len(dd.columns) == 9
    assert len(dd.index) == 50

def test_removing_tables(command):
    path = Path('spotify_data/tests/fixtures/unoptimized_data_sample.csv')
    dd = command.read_csv_dask_dataframe(path)
    dd = command.remove_irrelevant_columns(dd)

    assert len(dd.columns) == 7

    for column in DASK_COLUMNS_TO_DROP:
        assert column not in dd.columns


def test_dask_data_optimization_types(command):
    path = Path('spotify_data/tests/fixtures/unoptimized_data_sample.csv')
    dd = command.read_csv_dask_dataframe(path)
    dd = command.optimize_types_in_dask(dd)

    for column in DASK_COLUMNS_TO_CATEGORY:
        assert dd[column].dtype == "category"
    for column in DASK_COLUMNS_TO_DATETIME64:
        assert dd[column].dtype == "datetime64[ns]"
    for column in DASK_COLUMNS_TO_INT32:
        assert dd[column].dtype == "int32"


def test_dask_to_pandas(command):
    path = Path('spotify_data/tests/fixtures/unoptimized_data_sample.csv')
    dd = command.read_csv_dask_dataframe(path)
    df = command.dask_to_pandas(dd)
    
    assert type(df) is pd.DataFrame


def test_fillna_streams(command):
    path = Path('spotify_data/tests/fixtures/unoptimized_data_sample.csv')
    dd = command.read_csv_dask_dataframe(path)
    df = command.dask_to_pandas(dd)

    assert np.isnan(df.iloc[5,8])
    assert np.isnan(df.iloc[12,8])

    df = command.fill_na(df)
    
    assert df.iloc[5,8] == 0
    assert df.iloc[12,8] == 0    


def test_pandas_data_optimization_types(command):
    path = Path('spotify_data/tests/fixtures/to_test_optimize_types_in_pandas.csv')
    dd = command.read_csv_dask_dataframe(path)
    df = command.dask_to_pandas(dd)
    df = command.optimize_types_in_pandas(df)

    for column in PANDAS_COLUMNS_TO_INT32:
        assert df[column].dtype == "int32"


def test_drop_na(command):
    path = Path('spotify_data/tests/fixtures/to_test_drop_na.csv')
    dd = command.read_csv_dask_dataframe(path)
    df = command.dask_to_pandas(dd)

    assert len(df.index) == 50

    df = command.drop_na(df)

    assert len(df.index) == 47


def test_save_good_file(tmp_path, command):
    path = Path('spotify_data/tests/fixtures/to_test_save_file.csv')
    dd = command.read_csv_dask_dataframe(path)
    df = command.dask_to_pandas(dd)

    dir_path = tmp_path / "data_temp"
    filename = "file_temp.csv"
    file_path = dir_path / f"{filename}"
    dir_path.mkdir()
    command.save_file_as_csv(df, file_path, dir_path, filename)
  
    assert Path.is_file(file_path) and Path.exists(Path(file_path))


def test_save_file_wrong_dir(tmp_path, command):
    path = Path('spotify_data/tests/fixtures/to_test_save_file.csv')
    dd = command.read_csv_dask_dataframe(path)
    df = command.dask_to_pandas(dd)

    dir_path = tmp_path / Path("data_wrong")
    filename = "file_temp.csv"
    file_path = dir_path / f"{filename}"

    with pytest.raises(
        NotExistingDirectoryException,
        match="Cannot save file into a non-existent directory"
    ):
        command.save_file_as_csv(df, file_path, dir_path, filename)


def test_handle_input_right_path(tmp_path, command):
    path = Path('spotify_data/tests/fixtures/unoptimized_data_sample.csv')
    output = tmp_path / "data_temp"
    output.mkdir()
    filename = "file_temp.csv"
    file_path = output / f"{filename}"

    command.handle(path, output, filename)

    assert Path.is_file(file_path)

def test_handle_input_wrong_path(tmp_path, command):
    path = Path('non_existing_directory/unoptimized_data_sample.csv')
    output = tmp_path / "data_temp"
    output.mkdir()
    filename = "file_temp.csv"

    with pytest.raises(NoFilesException, match="No such file or directory"):
        command.handle(path, output, filename)