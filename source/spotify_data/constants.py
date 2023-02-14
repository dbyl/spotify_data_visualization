DEFAULT_COLUMNS = [
    "title",
    "rank",
    "date",
    "artist",
    "url",
    "region",
    "chart",
    "trend",
    "streams",
]

DASK_COLUMNS_TO_DROP = ["url", "trend"]

DASK_COLUMNS_TO_CATEGORY = ["title", "artist", "region", "chart"]

DASK_COLUMNS_TO_INT32 = ["rank"]

DASK_COLUMNS_TO_DATETIME64 = ["date"]

PANDAS_COLUMNS_TO_INT32 = ["streams"]

UNOPTIMIZABLE_COLUMNS = [
    "title",
    "rank",
    "date",
    "artist",
    "region",
    "chart",
    "streams",
]

PANDAS_COLUMNS_TO_TRIM_DATA = ["title", "artist"]

PANDAS_COLUMNS_TO_CATEGORY = ["title", "artist"]


REGIONS_ID_ISO = {
    1: "AND",
    2: "ARG",
    3: "AUS",
    4: "AUT",
    5: "BEL",
    6: "BOL",
    7: "BRA",
    8: "BGR",
    9: "CAN",
    10: "CHL",
    11: "COL",
    12: "CRI",
    13: "CZE",
    14: "DNK",
    15: "DOM",
    16: "ECU",
    17: "EGY",
    18: "SLV",
    19: "EST",
    20: "FIN",
    21: "FRA",
    22: "DEU",
    24: "GRC",
    25: "GTM",
    26: "HND",
    27: "HKG",
    28: "HUN",
    29: "ISL",
    30: "IND",
    31: "IDN",
    32: "IRL",
    33: "ISR",
    34: "ITA",
    35: "JPN",
    36: "LVA",
    37: "LTU",
    38: "LUX",
    39: "MYS",
    40: "MEX",
    41: "MAR",
    42: "NLD",
    43: "NZL",
    44: "NIC",
    45: "NOR",
    46: "PAN",
    47: "PRY",
    48: "PER",
    49: "PHL",
    50: "POL",
    51: "PRT",
    52: "ROU",
    53: "RUS",
    54: "SAU",
    55: "SGP",
    56: "SVK",
    57: "ZAF",
    58: "KOR",
    59: "ESP",
    60: "SWE",
    61: "CHE",
    62: "TWN",
    63: "THA",
    64: "TUR",
    65: "UKR",
    66: "ARE",
    67: "GBR",
    68: "USA",
    69: "URY",
    70: "VNM",
}
