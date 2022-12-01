import logging
import logging.config
from pathlib import Path
from typing import List

import pandas as pd
from django.core.management.base import BaseCommand

from spotify_data.constants import DEFAULT_COLUMNS, COLUMNS_TO_DROP, UNOPTIMIZABLE_COLUMNS
from spotify_data.exceptions import (NoFilesException,
                                     NotExistingDirectoryException,
                                     WrongFileTypeException)
from spotify_data.models import SpotifyData



class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "input", type=str, help="Directory path with input csv files"
        )

        parser.add_argument(
            "output", type=str, help="Directory path with output csv files"
        )

    def handle(self, input, output, *args, **options):
        