import datetime
import logging
import logging.config

import pandas as pd
from django.core.management import BaseCommand
from spotify_data.models import Artist, Chart, Rank, Region, SpotifyData, Title


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
        return df

    def load_to_db(self, df):
        bad = 0
        good = 0
        start = datetime.datetime.now
        for _, row in df.iterrows():
            try:
                region_obj, _ = Region.objects.get_or_create(
                    name=row["region"],
                )
                rank_obj, _ = Rank.objects.get_or_create(
                    name=row["rank"],
                )
                chart_obj, _ = Chart.objects.get_or_create(
                    name=row["chart"],
                )
                artist_obj, _ = Artist.objects.get_or_create(
                    name=row["artist"],
                )
                title_obj, _ = Title.objects.update_or_create(
                    artist=artist_obj,
                    name=row["title"],
                )
                spotifydata_obj, _ = SpotifyData.objects.update_or_create(
                    title=title_obj,
                    rank=rank_obj,
                    date=row["date"],
                    artist=artist_obj,
                    region=region_obj,
                    chart=chart_obj,
                    streams=row["streams"],
                )
                good += 1
                now = datetime.datetime.now
                print(
                    f"goods: {good}, loading time: {start-now}",
                )
            except Exception as e:
                bad += 1
                with open("data_load_logging.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {e} \n")
