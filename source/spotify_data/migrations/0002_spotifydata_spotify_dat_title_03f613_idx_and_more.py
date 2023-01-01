# Generated by Django 4.1.3 on 2023-01-01 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_data', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='spotifydata',
            index=models.Index(fields=['title'], name='spotify_dat_title_03f613_idx'),
        ),
        migrations.AddIndex(
            model_name='spotifydata',
            index=models.Index(fields=['rank'], name='spotify_dat_rank_030c94_idx'),
        ),
        migrations.AddIndex(
            model_name='spotifydata',
            index=models.Index(fields=['date'], name='spotify_dat_date_8c1cfa_idx'),
        ),
        migrations.AddIndex(
            model_name='spotifydata',
            index=models.Index(fields=['artist'], name='spotify_dat_artist_ac3869_idx'),
        ),
        migrations.AddIndex(
            model_name='spotifydata',
            index=models.Index(fields=['region'], name='spotify_dat_region_4e1779_idx'),
        ),
        migrations.AddIndex(
            model_name='spotifydata',
            index=models.Index(fields=['chart'], name='spotify_dat_chart_f59dab_idx'),
        ),
    ]
