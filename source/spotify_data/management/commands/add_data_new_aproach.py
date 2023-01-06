from spotify_data.models import (Region,
                                 Rank,
                                 Chart,
                                 Artist,
                                 Title,
                                 ArtistTitle,
                                 SpotifyData)

import csv
import datetime
import logging
import logging.config

from django.core.management import BaseCommand
from django.utils import timezone
from spotify_data.exceptions import (NoFilesException,
                                     NotExistingDirectoryException,
                                     WrongFileTypeException)
from spotify_data.models import SpotifyData


class Command(BaseCommand):

    help = "A command to add data from a csv file to the database."

    def add_arguments(self, parser):
        parser.add_argument("input", type=str, help="Choose path with input csv files")

    def handle(self, input, *args, **options):

        logging.info(f"Preparing data from {input}...")
        self.load_to_db(input)

    def load_to_db(self, path):
        start_time = timezone.now()
        try:
            with open(path, "r") as csv_file:
                data = csv.reader(csv_file)
                packet_region = []
                packet_rank = []
                packet_chart = []
                packet_artist = []
                packet_title = []
                packet_artist_title = [] 
                packet_spotify_data = []
                bad = -1  # first row is a header
                for row in data:
                    try:
                        region = Region(
                            region = row[0]
                        )

                        rank = Rank(
                            rank = int(row[0])
                        )

                        chart = Chart(
                            chart = row[0]
                        )

                        artist = Artist(
                            artist = row[0]
                        )

                        title = Title(
                            title = row[0]
                        )

                        artist_title = ArtistTitle(
                            artist = artist,
                            title = title
                        )

                        spotify_data = SpotifyData(
                            title = title,
                            rank = rank,
                            date = row[2],
                            artist = artist,
                            region = region,
                            chart = chart,
                            streams = int(row[6])
                        )

                        packet_region.append(region)
                        packet_rank.append(rank)
                        packet_chart.append(chart)
                        packet_artist.append(artist)
                        packet_title.append(title)
                        packet_artist_title.append(artist_title)
                        packet_spotify_data.append(spotify_data)
                        if len(packet_spotify_data) > 10000:
                            print(datetime.datetime.now())
                            Region.objects.bulk_create(packet_region)
                            Rank.objects.bulk_create(packet_rank)
                            Chart.objects.bulk_create(packet_chart)
                            Artist.objects.bulk_create(packet_artist)
                            Title.objects.bulk_create(packet_title)
                            ArtistTitle.objects.bulk_update(packet_artist_title)
                            SpotifyData.objects.bulk_update(packet_spotify_data)
                            packet_region = []
                            packet_rank = []
                            packet_chart = []
                            packet_artist = []
                            packet_title = []
                            packet_artist_title = [] 
                            packet_spotify_data = []
                    except Exception as e:
                        bad += 1
                        current_time = datetime.datetime.now()
                        with open("data_load_logging.txt", "w") as bad_row:
                            bad_row.write(
                                f"Error message: {e} \n"
                            )
                logging.info(f"Failure numbers: {bad}")
                if packet_spotify_data:
                    Region.objects.bulk_create(packet_region)
                    Rank.objects.bulk_create(packet_rank)
                    Chart.objects.bulk_create(packet_chart)
                    Artist.objects.bulk_create(packet_artist)
                    Title.objects.bulk_create(packet_title)
                    ArtistTitle.objects.bulk_update(packet_artist_title)
                    SpotifyData.objects.bulk_update(packet_spotify_data)
        except FileNotFoundError as e:
            raise NoFilesException("No such file or directory") from e

        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
            )
        )
