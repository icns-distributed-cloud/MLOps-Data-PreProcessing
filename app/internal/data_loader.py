import os
import pandas as pd
import numpy as np

from app.models.exceptions import *

def load_csv_data(filename):
    try:
        try:
            df = pd.read_csv(filename, encoding='gbk')
        except:
            df = pd.read_csv(filename, encoding='utf-8')
    except FileNotFoundError as e:
        raise NotFoundDataEx(ex=e)
    except Exception as e:
        raise APIException(ex=e)
    return df