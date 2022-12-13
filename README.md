# Spotify Data Visualization

## Introduction

The program will be used to visualize data about top200 and viral50 charts published globally by Spotify.

Players data are collected from FIFA databases prepared 
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

---

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
$ docker-compose -f docker-compose.yaml up --build
```

Docker-server should be started.

To test test management commands during application running open new terminal window and run:
```sh
(env)$ docker exec -it spotify_data_visualization_web_1 /bin/bash  
(env)$ python3 -m pytest source/spotify_data/tests/tests_prepare_optimize_data.py
(env)$ python3 -m pytest source/spotify_data/tests/tests_add_data_via_raw_csv.py
```

Before next steps you to download dataset from: https://www.kaggle.com/datasets/dhruvildave/spotify-charts
,create directory in source/spotify_data named "data" and paste there spotify_charts.csv. 

To transfortm data from raw csv file run:
```sh
(env)$ docker exec -it spotify_data_visualization_web_1 /bin/bash  
(env)$ python3 source/manage.py prepare_optimize_data spotify_data/data/spotify_charts.csv spotify_data/data/ spotify_charts.csv
```

To load data from optimized csv:
```sh
(env)$ docker exec -it spotify_data_visualization_web_1 /bin/bash  
(env)$ python3 source/manage.py add_data_via_raw_csv spotify_data/data/spotify_charts.csv
```



