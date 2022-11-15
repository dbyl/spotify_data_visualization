# Generated by Django 4.1.3 on 2022-11-15 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_data', '0002_alter_spotifydata_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifydata',
            name='rank',
            field=models.DecimalField(decimal_places=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='spotifydata',
            name='streams',
            field=models.DecimalField(decimal_places=0, max_digits=50),
        ),
    ]
