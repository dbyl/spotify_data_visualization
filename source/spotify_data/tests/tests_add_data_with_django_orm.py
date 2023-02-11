import os
from pathlib import Path

import pytest
from spotify_data.exceptions import NoFilesException
from spotify_data.management.commands.add_data_with_django_orm import Command
from spotify_data.models import Artist, Chart, Rank, Region, SpotifyData, Title


@pytest.fixture
def command():
    return Command()


@pytest.mark.django_db
def test_load_spotify_datas_to_db_with_succeed(command):

    input = Path("source/spotify_data/tests/fixtures/to_test_add_data.csv")
    df = command.read_csv(input)
    data = command.load_to_db(df)

    artist_1 = Artist.objects.get(id=1)
    artist_2 = Artist.objects.get(name="Maluma")

    title_1 = Title.objects.get(name="Borro Cassette", artist=13)

    assert artist_1.name == "Shakira"
    assert artist_2.id == 13
    assert title_1.id == 13
