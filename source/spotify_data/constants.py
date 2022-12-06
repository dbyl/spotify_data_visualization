DEFAULT_COLUMNS = [
    "title",
    "rank",
    "date",
    "artist",
    "url",
    "region",
    "chart",
    "trend",
    "streams"
]

DASK_COLUMNS_TO_DROP = [
    "url",
    "trend"
]

DASK_COLUMNS_TO_CATEGORY = [
    "title", 
    "artist", 
    "region",  
    "chart"
]

DASK_COLUMNS_TO_INT32 = [
    "rank"
]

DASK_COLUMNS_TO_DATETIME64 = [
    "date"
]

PANDAS_COLUMNS_TO_INT32 = [ 
    "streams"   
]

UNOPTIMIZABLE_COLUMNS = [
    "title",
    "rank",
    "date",
    "artist",
    "region",
    "chart",
    "streams" 
]
    
