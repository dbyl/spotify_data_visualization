import csv
import pandas as pd
from django.core.management import BaseCommand
from django.utils import timezone
from spotify_data.models import SpotifyData

"""class Command(BaseCommand):
    
    help = "A command to add data from a csv file to the database."
    
    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        start_time = timezone.now()
        file_path = options["file_path"]
        with open(file_path, "r") as csv_file:
            data = csv.reader(csv_file, delimiter=",")
            all_spotify_data = []
            for row in data:
                spotify_data = SpotifyData(
                    title=row[0],
                    rank=int(row[1]),
                    date=row[2],
                    artist=row[3],
                    region=row[4],
                    chart=row[5],
                    streams=int(row[6])
                    )
                all_spotify_data.append(spotify_data)
                if len(all_spotify_data) > 5000:
                    SpotifyData.objects.bulk_create(all_spotify_data)
                    all_spotify_data = []
            if all_spotify_data:
                SpotifyData.objects.bulk_create(all_spotify_data)
        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
            )
        )
    """
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
        return df

    def load_to_db(self, df):
        for _, row in df.iterrows():           
            row, _ = SpotifyData.objects.get_or_create(
                title=row["title"],
                rank=int(row["rank"]),
                date=row["date"],
                artist=row["artist"],
                region=row["region"],
                chart=row["chart"],
                streams=int(row["streams"])
            )

            