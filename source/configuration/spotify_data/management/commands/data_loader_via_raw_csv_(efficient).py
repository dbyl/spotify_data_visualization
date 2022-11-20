import csv
from django.core.management import BaseCommand
from django.utils import timezone
from spotify_data.models import SpotifyData
import datetime

class Command(BaseCommand):
    
    help = "A command to add data from a csv file to the database."
    
    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        start_time = timezone.now()
        file_path = options["file_path"]
        with open(file_path, "r") as csv_file:
            data = csv.reader(csv_file)
            packet_spotify_data = []
            bad = -1 #first row is a header
            for row in data:
                try:
                    spotify_data = SpotifyData(
                        title=row[0],
                        rank=int(row[1]),
                        date=row[2],
                        artist=row[3],
                        region=row[4],
                        chart=row[5],
                        streams=int(row[6])
                        )
                    packet_spotify_data.append(spotify_data)
                    if len(packet_spotify_data) > 5000:
                        print(datetime.datetime.now())
                        SpotifyData.objects.bulk_create(packet_spotify_data)
                        packet_spotify_data = []
                except Exception as e:
                    bad += 1
                    current_time = datetime.datetime.now()
                    with open("data_load_logging2.txt", "w") as bad_row:
                        bad_row.write(f"Error message: {e} \n"
                                  + f"time: {current_time}, \n"
                                  + f"title: {row[0]}, type: {row[0]} \n"
                                  + f"rank: {row[1]}, type: {row[1]} \n" 
                                  + f"date: {row[2]}, type: {row[2]} \n"
                                  + f"artist: {row[3]}, type: {row[3]} \n"
                                  + f"region: {row[4]}, type: {row[4]} \n" 
                                  + f"chart: {row[5]}, type: {row[5]} \n"
                                  + f"streams: {row[6]}, type: {row[6]} \n"
                                  + "-"*30
                                  + "\n")
            print(bad)
            if packet_spotify_data:
                SpotifyData.objects.bulk_create(packet_spotify_data)
        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
            )
        )
    