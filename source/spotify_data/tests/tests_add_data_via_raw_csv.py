import os
from pathlib import Path

import pytest
from spotify_data.exceptions import NoFilesException
from spotify_data.management.commands.add_data_via_raw_csv import Command
from spotify_data.models import SpotifyData


@pytest.fixture
def command():
    return Command()


@pytest.mark.django_db
def test_load_spotify_datas_to_db_with_succeed(command, **options):

    input = Path(
        "source/spotify_data/tests/fixtures/to_test_add_data.csv"
    )
    spotify_data = command.handle(input)
    record_1 = SpotifyData.objects.get(artist="Shakira")

    assert record_1.title == "Chantaje (feat. Maluma)"

    record_1.delete()
