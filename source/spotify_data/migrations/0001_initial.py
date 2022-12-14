# Generated by Django 4.1.3 on 2022-12-20 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SpotifyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('rank', models.IntegerField()),
                ('date', models.DateField()),
                ('artist', models.CharField(max_length=60)),
                ('region', models.CharField(max_length=20)),
                ('chart', models.CharField(max_length=8)),
                ('streams', models.IntegerField()),
            ],
        ),
    ]
