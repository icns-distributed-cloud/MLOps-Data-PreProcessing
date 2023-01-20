from fastapi import BackgroundTasks

from app.models.exceptions import *

from scipy.stats import pearsonr

import os
import pandas as pd
import numpy as np
import time

def load_csv_data(filename):
    try:
        df = pd.read_csv(filename, encoding='gbk')
    except FileNotFoundError as e:
        raise NotFoundDataEx(ex=e)
    except Exception as e:
        raise APIException(ex=e)
    return df


def save_csv_data(df, filename):
    try:
        df.to_csv(filename, index=False)
    except Exception as e:
        raise APIException(ex=e)
    return filename, True


def valid_columns(columns, origin_columns):
    try:
        for column in columns:
            if column not in origin_columns:
                raise NotFoundColumnEx()
    except Exception as e:
        raise APIException(ex=e)


def get_pearsonr(data, columns):
    origin_columns = data.columns

    pearson_dict = {}
    for column in columns:
        for origin_column in origin_columns:
            pearsonr(data[column], data[origin_column])


def save_mini_data(filename, nrows=50):
    try:
        path, file = os.path.split(filename)
        mini_path = change_path(path, 'origin', 'mini')
 
        df = pd.read_csv(filename, nrows=nrows)
        
        save_csv_data(df, f'{mini_path}/{file}')
    except Exception as e:
        raise APIException(ex=e)
    return df


def change_path(path, source, target):
    path = path.replace(source, target)

    return path