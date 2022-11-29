import csv
import datetime

import pandas as pd
from django.core.management import BaseCommand
from django.utils import timezone
from spotify_data.models import SpotifyData


class Command(BaseCommand):

    help = "A command to add data from a csv file to the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "input", type=str, help="Choose directory path with input csv files"
        )

    def handle(self, *args, **options):

        path = options["input"]

        df = self.read_csv(path)
        self.load_to_db(df)

    def read_csv(self, directory):
        df = pd.read_csv(directory)
        return df[0:1000]

    def load_to_db(self, df):
        bad = 0
        for _, row in df.iterrows():
            try:
                obj, _ = SpotifyData.objects.get_or_create(
                    title=row["title"],
                    rank=int(row["rank"]),
                    date=row["date"],
                    artist=row["artist"],
                    region=row["region"],
                    chart=row["chart"],
                    streams=int(row["streams"]),
                )
                print("good", datetime.datetime.now)
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
        print(bad)
