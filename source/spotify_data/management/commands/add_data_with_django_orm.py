import csv
import datetime
import logging
import logging.config

import pandas as pd
from django.core.management import BaseCommand
from django.utils import timezone
from spotify_data.models import (SpotifyData,
                     Region,
                     Rank,
                     Chart,
                     Artist,
                     Title,
                     ArtistTitle)


class Command(BaseCommand):

    help = "A command to add data from a csv file to the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "input", type=str, help="Choose directory path with input csv files"
        )

    def handle(self, *args, **options):

        path = options["input"]
        logging.info(f"Preparing data from {path}...")
        df = self.read_csv(path)
        self.load_to_db(df)

    def read_csv(self, directory):
        df = pd.read_csv(directory)
        return df[0:1000]

    def load_to_db(self, df):
        bad = 0
        good = 0
        start = datetime.datetime.now
        for _, row in df.iterrows():
            try:
                region_obj, _ = Region.objects.get_or_create(
                    region=row["region"],
                )
                rank_obj, _ = Rank.objects.get_or_create(
                    rank=row["rank"],
                )
                chart_obj, _ = Chart.objects.get_or_create(
                    chart=row["chart"],
                )
                artist_obj, _ = Artist.objects.get_or_create(
                    artist=row["artist"],
                )
                title_obj, _ = Title.objects.get_or_create(
                    title=row["title"],
                )
                arttit_obj, _ = ArtistTitle.objects.update_or_create(
                    artist=artist_obj,
                    title=title_obj,
                )
                spotifydata_obj, _ = SpotifyData.objects.update_or_create(
                    title=arttit_obj,
                    rank=rank_obj,
                    date=row["date"],
                    artist=arttit_obj,
                    region=region_obj,
                    chart=chart_obj,
                    streams=row["streams"],
                )
                good += 1
                now = datetime.datetime.now
                print(f"goods: {good}, loading time: {start-now}", )
            except Exception as e:
                bad += 1
                current_time = datetime.datetime.now()
                with open("data_load_logging.txt", "w") as bad_row:
                    bad_row.write(
                        f"Error message: {e} \n"
                        + f"time: {current_time}, \n"
                        + f"title: {row['title']}, type: {row['title']} \n"
                        + f"rank: {int(row['rank'])}, type: {int(row['rank'])} \n"
                        + f"date: {row['date']}, type: {row['date']} \n"
                        + f"artist: {row['artist']}, type: {row['artist']} \n"
                        + f"region: {row['region']}, type: {row['region']} \n"
                        + f"chart: {row['chart']}, type: {row['chart']} \n"
                        + f"streams: {int(row['streams'])}, type: {int(row['streams'])} \n"
                        + "-" * 30
                        + "\n"
                    )
