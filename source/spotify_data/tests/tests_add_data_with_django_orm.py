import os
from pathlib import Path

import pytest
from spotify_data.exceptions import NoFilesException
from spotify_data.management.commands.add_data_with_django_orm import Command
from spotify_data.models import (SpotifyData,
                                    Region,
                                    Rank,
                                    Chart,
                                    Artist,
                                    Title,
                                    ArtistTitle)


@pytest.fixture
def command():
    return Command()


@pytest.mark.django_db
def test_load_spotify_datas_to_db_with_succeed(command, **options):

    input = Path(
        "source/spotify_data/tests/fixtures/to_test_add_data.csv"
    )
    artist = command.handle(input)
    artist_1 = Artist.objects.get(artist="Shakira")
    artist_1_filtered= Artist.objects.filter(artist=artist_1)


    assert artist_1_filtered.id == 1

    
