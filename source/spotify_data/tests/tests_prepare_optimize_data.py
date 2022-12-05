from pathlib import Path

import pandas as pd
from dask import dataframe as dd
import pytest

from spotify_data.exceptions import NoFilesException
from spotify_data.management.commands.prepare_optimize_data import Command


@pytest.fixture
def command():
    return Command()


def test_read_csv_with_proper_amount_of_columns_rows(command):
    path = Path('fixtures/unoptimized_data_sample.csv')
    dd = command.read_csv_dask_dataframe(path)

    assert len(dd.columns) == 9
    assert len(dd.index) == 50

def test_removing_tables(command):
    pass 

def test_data_optimization_types(command):
    pass

def test_save_correct_file(command):
    pass