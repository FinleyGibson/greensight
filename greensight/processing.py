
from typing import Callable, Union
from pathlib import Path
import re
import pandas as pd
from greensight.utils import DIR_DATA
from datetime import datetime
import json
import numpy as np


def load_sentinel_data_from_dir(path: Union[str, Path], condition: Callable):
    path = Path(path)
    assert path.is_dir()

    # Extract the year using regex
    match = re.search(r"\d{4}", str(path))
    year = int(match.group(0) if match else None)

    # get all files which meet the stipulated condition
    files = sorted([file for file in path.iterdir() if condition(file)])

    # load and concatenate
    data = [pd.read_csv(file) for file in files]
    df = pd.concat(data, axis=0)

    # get unique band identifiers
    band_inds = pd.unique([i.split("_")[1] for i in df.columns.unique() if i.split("_")[0].isnumeric()])
    
    # get month identifiers
    month_inds = pd.unique([i.split("_")[0] for i in df.columns.unique() if i.split("_")[0].isnumeric()])

    # index by shape code
    df.index = df["LAD_CD"]

    # drop unwanted columns
    df = df.drop(columns=["system:index", ".geo"])

    months = []
    inds = []
    for month in month_inds:

        # generate desired columns
        cols = [month+"_"+band for band in band_inds]

        # create df of desired columns 
        df_month = df[cols].copy()

        # convert from a DataFrame of rows: shapes, columns: bands for a single month 
        # to a single row of rows: month, columns: (shape, band)
        row_month = df_month.stack().to_frame().T

        # create multi-index for the columns (shape, band)
        new_cols = [(a, b.split("_")[1]) for a, b in row_month.columns]
        row_month.columns = pd.MultiIndex.from_tuples(new_cols)

        # add to stack
        if row_month.shape[1] == 740:
            months.append(row_month)
            # add month name to index. 
            inds.append(month)
        else:
            # row is missing data 
            pass

    df_month = pd.concat(months, axis=0)
    df_month.index = np.array(inds).astype(int) + 1

    df_month = df_month.sort_index()
    df_month.index.name = "date"
    df_month.index = [datetime(year, int(month), 1) for month in df_month.index]
    df_month.columns.names =  ("shape", "band")

    # add greenbelt information from json dict. 
    lookup_path = DIR_DATA / "id_lookup/id_lookup.json"
    with open(lookup_path, "r") as in_file:
        D_lookup = json.load(in_file)
    greenbelts = [D_lookup[code] for code, band in df_month.columns]

    # add greenbelts to column MultiIndex
    df_month.columns = pd.MultiIndex.from_tuples([(gb, *cols) for gb, cols in zip(greenbelts, df_month.columns)])
    df_month.columns.names =  ("greenbelt", "shape", "band")

    return df_month