# Spotify Data Visualization

## Introduction

The program will be used to visualize data about top200 and viral50 charts published globally by Spotify.

Dataset is made by a member of the kaggle.com community: https://www.kaggle.com/datasets/dhruvildave/spotify-charts
Databases are separated by days for each, from 01.01.2017 to 31.12.2021. 

The project consists of two parts: 
1) Spotify Data overview and preparation of charts to be used in the application - that part is completed. 
2) Implementation of Django and creation usable program allowing the user to decide what data to include in the charts.

## 1 part - Spotify Data Overview 


Because of the large amount of data, it was necessary to open and optimize data with Dask before exploring data in Pandas Dataframe. The dataset overview was proceeded in Jupyter Notebook with graph made with Plotly Express.

*Sample images of charts from Jupyter Notebook Analysis*

Top streamed songs in choosen region
![](images/top_streamed_regions_c.png)

Top streamed artists in choosen regions
![](images/top_streamed_art_reg_com.png)

Songs occurance in ranking comparison for choosen region
![](images/songs_occur_in_rank_com.png)

Percentage share of artist in all streams (world map)
![](images/per_share_artist_map.png)

Songs rank changes over time
![](images/song_rank_changes_com.png)


## 2 part - Django App implementation 



## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/dbyl/spotify_data_visualization
$ cd spotify_data_visualization
```

This project requires Python 3.6 or later.

Create a virtual environment to install dependencies in and activate it:

Linux:
```sh
$ python3 -m venv env
$ source env/bin/activate
```

Create a .env file in project root directory (source). The file format can be understood from the example below:
```sh
DEBUG=True
SECRET_KEY=your-secret-key # generate your own secret key
DATABASE_URL=psql://postgres:postgres@database:5432/postgres
ALLOWED_HOSTS=127.0.0.1,localhost
```

Application runs on docker so docker must be configured *(sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin)* and Docker Desktop must be installed.
Please open Docker Desktop and run docker-compose to install dependiences and run application:
```sh
(env)$ docker-compose -f docker-compose.yaml up --build
```

Docker-server should be started.


To test management commands during application running open new terminal window and run:
```sh
(env)$ docker exec -it spotify_data_visualization_web_1 /bin/bash
(env)$ python3 -m pytest source/spotify_data/tests/tests_prepare_optimize_data.py
(env)$ python3 -m pytest source/spotify_data/tests/tests_add_data_via_raw_csv.py
```

Before next steps you have to download dataset from: https://www.kaggle.com/datasets/dhruvildave/spotify-charts
,create directory in source/spotify_data named "data" and paste there spotify_charts.csv. 


If project is setting up for the first time make sure that in source/spotify_data/makemigrations exists only one file - __init__.py. 
To make migrations and create superuser run:
```sh
(env)$ docker exec -it spotify_data_visualization-web-1 /bin/bash
(env)$ python3 source/manage.py migrate
(env)$ python3 source/manage.py makemigrations
(env)$ python3 source/manage.py sqlmigrate spotify_data 0001
(env)$ python3 source/manage.py createsuperuser
(env)$ python3 source/manage.py migrate
```

To transfortm data from raw csv file run:
```sh
(env)$ docker exec -it spotify_data_visualization-web-1 /bin/bash
(env)$ python3 source/manage.py prepare_optimize_data source/spotify_data/data/spotify_charts.csv source/spotify_data/data/ spotify_charts.csv
```

## Data loading

There are two ways of inserting such a large csv file into a relational database. 

-------DJANGO ORM METHOD-------

The first method is simpler to implement and to understand how it works. This way uses django orm and matches data to individual tables row by row.
A significant drawback is its slow performance. It will take about 65 hours to upload the entire database using this method. 

-------POSTGRESQL METHOD-------

The second method is more difficult to implement and setting up the environment will take additional time. 
This way uses direct upload to postgresql using pgadmin4 and client-side terminal. 
Uploading data this way should take about 30 minutes until all the queries are done, which is a significant advantage. 

# DJANGO ORM METHOD

To load data from optimized csv:
```sh
(env)$ docker exec -it spotify_data_visualization-web-1 /bin/bash 
(env)$ python3 source/manage.py add_data_with_django_orm source/spotify_data/data/spotify_charts.csv
```

# POSTGRESQL METHOD

1) Increasing max_wal_size and min_wal_size

To handle all queries max_wal_size and min_wal_size must be increased. To do this you need to edit the postgresql configuration file located in the postgres:14.2-alpine container. There are several methods to do it.

The easiest way is to install the Docker extension in VSC and then edit the */var/lib/postgresql/postgresql.conf* file in *VSC/Docker/CONTAINERS/spotify_data_visualization/postgres:14.2-alpine*. 

Find:
```sh
max_wal_size = 1GB
min_wal_size = 80MB
```

And change to:
```sh
max_wal_size = 8GB
min_wal_size = 2GB
```

Save the file.

2) Loading csv file into *postgres:14.2-alpine* container

In order for postgres to access the file from which data will be uploaded to the database, it must be in the same container.

To copy a csv file to a container follow these steps.

Open new terminal window and run:

```sh
(env)$ docker container ls
```

Find *postgres:14.2-alpine* container and copy it's *CONTAINER ID*:

```sh
(env)$ docker cp source/spotify_data/data/spotify_charts.csv CONTAINER_ID:/var/lib/postgresql/data/spotify_charts.csv
```

3) Saving changes

In order for the changes to be applied, all containers in Docker Desktop must be stopped and reloaded with the command: 

```sh
(env)$ docker-compose -f docker-compose.yaml up --build
```

Using Docker Extension make sure that the changes are saved. 

There should be a *spotify_charts.csv* file in the */var/lib/postgresql/data* directory.

4) Loading data

To start, you need to get a bash shell in the *postgres:14.2-alpine* container running.

Open new terminal window and run:
```sh
(env)$ docker exec -it spotify_data_visualization_database_1 /bin/bash
```

Then open Postgres terminal by command:
```sh
(env)$ psql -U postgres
```

From now on you are in the postgresql terminal.

Make sure that:

```sh
max_wal_size = 8GB
min_wal_size = 2GB
```

By:

```sh
(env)$ select name, setting from pg_settings where name like '%wal_size%' or name like '%checkpoint%' order by name;
```

Create a table into which all data from the csv file will be dumped:

```sh
(env)$ create table objects_landing (title VARCHAR(60), "rank" INT, "date" DATE, artist VARCHAR(60), region VARCHAR(20), chart VARCHAR(8), streams INT);
```

And copy csv data into the table:

```sh
(env)$ \copy objects_landing from '/var/lib/postgresql/data/spotify_charts.csv' csv header;
```

Wait until all the data has been copied.

5) Connecting pgadmin4 with postgresql database

Open new terminal window and run:
```sh
(env)$ docker container ls
```

Find *postgres:14.2-alpine* container and copy it's *CONTAINER ID*:

```sh
(env)$ docker inspect CONTAINER ID
```

Find at the very bottom *"Networks": {"IPAddress": "IP"}* and copy *IP*.

Open http://127.0.0.1:5050/ and log in with root@root.com / root.

Go to the Dashboard and Add New Server. 

>General/Name: spotify
>Connection/Host name/address: *IP*
>Connection/Username: postgres
>Connection/Password: postgres

Save that. 

Go to Browser -> Servers(1) -> spotify -> Databases (1) ->  postgres -> Schemas (1) -> public -> Tables (18)

You should see the list of 18 tables.

Click once on Tables(18) and Alt+Shift+Q, the Query Tool window should appear.

6) Executing queries

Being in the Query Tool window type:

```sql
INSERT INTO spotify_data_artist (artist)
SELECT DISTINCT artist FROM objects_landing ORDER BY (artist) ASC;

INSERT INTO spotify_data_title (title, artist_id)
SELECT sq.title, 
sq.artist_id
FROM
(SELECT DISTINCT ol.title,
ar.id AS artist_id
FROM objects_landing AS ol 
LEFT JOIN spotify_data_artist AS ar ON ol.artist = ar.artist
) AS sq ORDER BY title ASC;

INSERT INTO spotify_data_chart (chart)
SELECT DISTINCT chart FROM objects_landing ORDER BY (chart) ASC;

INSERT INTO spotify_data_rank ("rank")
SELECT DISTINCT "rank" FROM objects_landing ORDER BY ("rank") ASC;

INSERT INTO spotify_data_region (region)
SELECT DISTINCT region FROM objects_landing ORDER BY (region) ASC;
```

Press F5 or "Play Button" to execute. 
It should take about 30-40 seconds to execute.
After query completed type next query:

```sql
INSERT INTO spotify_data_spotifydata (date, streams, rank_id, region_id, chart_id, artist_id, title_id)
SELECT sq.date, 
sq.streams,
sq.rank_id,
sq.region_id,
sq.chart_id,
sq.artist_id,
sq.title_id
FROM
(SELECT ol.date, 
ol.streams, 
rk.id AS rank_id,
rg.id AS region_id,
ch.id AS chart_id,
ar.id AS artist_id,
ti.id AS title_id
FROM objects_landing AS ol 
LEFT JOIN spotify_data_rank AS rk ON ol.rank = rk.rank
LEFT JOIN spotify_data_region AS rg ON ol.region = rg.region
LEFT JOIN spotify_data_chart AS ch ON ol.chart = ch.chart
LEFT JOIN spotify_data_artist AS ar ON ol.artist = ar.artist
LEFT JOIN spotify_data_title AS ti ON ol.title = ti.title AND ol.artist = ar.artist AND ar.id = ti.artist_id)
AS sq;
```

Press F5 or "Play Button" to execute. 
It should take about 30 minutes to execute.

To safe some space you can remove the unnecessary column by query:

```sql
DROP TABLE objects_landing;
```

All the data should now be in the database.