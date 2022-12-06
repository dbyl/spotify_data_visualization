import logging
import logging.config
import csv
import datetime

from django.core.management import BaseCommand
from django.utils import timezone
from spotify_data.exceptions import (NoFilesException,
                                     NotExistingDirectoryException,
                                     WrongFileTypeException)
from spotify_data.models import SpotifyData


class Command(BaseCommand):

    help = "A command to add data from a csv file to the database."

    def add_arguments(self, parser):
        parser.add_argument("input", type=str, help='Choose path with input csv files')

    def handle(self, input, *args, **options):

        logging.info(f"Preparing data from {input}...")
        self.load_to_db(input)
    
    def load_to_db(self, path):
        start_time = timezone.now()
        try:
            with open(path, "r") as csv_file:
                data = csv.reader(csv_file)
                packet_spotify_data = []
                bad = -1  # first row is a header
                for row in data:
                    try:
                        spotify_data = SpotifyData(
                            title=row[0],
                            rank=int(row[1]),
                            date=row[2],
                            artist=row[3],
                            region=row[4],
                            chart=row[5],
                            streams=int(row[6]),
                        )
                        packet_spotify_data.append(spotify_data)
                        if len(packet_spotify_data) > 5000:
                            print(datetime.datetime.now())
                            SpotifyData.objects.bulk_create(packet_spotify_data)
                            packet_spotify_data = []
                    except Exception as e:
                        bad += 1
                        current_time = datetime.datetime.now()
                        with open("data_load_logging.txt", "w") as bad_row:
                            bad_row.write(
                                f"Error message: {e} \n"
                                + f"time: {current_time}, \n"
                                + f"title: {row[0]}, type: {row[0]} \n"
                                + f"rank: {row[1]}, type: {row[1]} \n"
                                + f"date: {row[2]}, type: {row[2]} \n"
                                + f"artist: {row[3]}, type: {row[3]} \n"
                                + f"region: {row[4]}, type: {row[4]} \n"
                                + f"chart: {row[5]}, type: {row[5]} \n"
                                + f"streams: {row[6]}, type: {row[6]} \n"
                                + "-" * 30
                                + "\n"
                            )
                logging.info(f"Failure numbers: {bad}")
                if packet_spotify_data:
                    SpotifyData.objects.bulk_create(packet_spotify_data)
        except FileNotFoundError as e:
            raise NoFilesException("No such file or directory") from e

        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
            )
        )
