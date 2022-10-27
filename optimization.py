import pandas as pd
from dask import dataframe as dd


def read_csv_as_dask_dataframe(path):
    
    dask_dataframe = dd.read_csv(path, 
                     dtype=object)
    
    return dask_dataframe


def optimize_types_in_dask_dataframe(dask_dataframe):
     
    to_category_cols = ['title', 'url', 'date', 'artist', 'region', 'trend', 'chart']
    to_int32_cols = ['rank']
    
    for col in to_category_cols:
        dask_dataframe[col] = dask_dataframe[col].astype('category')
        
    for col in to_int32_cols:
        dask_dataframe[col] = dask_dataframe[col].astype('int32')
    
    return dask_dataframe

def dask_to_pandas_dataframe(dask_dataframe):
    
    dataframe = dask_dataframe.compute()
    
    return dataframe

def optimize_dataframe(dataframe):
    
    dataframe['streams'].fillna(value=0, inplace=True)
    dataframe['streams'] = dataframe['streams'].astype('int32')
    dataframe.dropna(inplace=True)
    
    return dataframe

