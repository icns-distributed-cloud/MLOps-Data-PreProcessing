from fastapi import BackgroundTasks

from app.models.exceptions import *
from app.internal.restAPI import *

from scipy.stats import pearsonr
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import os
import pandas as pd
import numpy as np
import time

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


def save_csv_data(df, filename):
    try:
        if filename[-4:] != '.csv':
            filename += '.csv'

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


def save_mini_data(file_path, source, target, db_id, nrows=50, is_origin=False):
    try:
        path, file_name = os.path.split(file_path)
        save_path = change_path(path, source, target)
        save_path = 'datasets/mini'
        try:
            df = pd.read_csv(file_path, nrows=nrows)
        except:
            df = pd.read_csv(file_path, nrows=nrows, encoding='utf-8')
        
        if is_origin == True:
            save_csv_data(df, f'{save_path}/{db_id}_{file_name}')
            mini_path = f'{save_path}/{db_id}_{file_name}'
        else:
            save_csv_data(df, f'{save_path}/{file_name}')
            mini_path = f'{save_path}/{file_name}'
    
        mini_path = mini_path.replace('./', '')
        update_readpre_path(db_id, f'/{mini_path}')

        sns.set(rc={'font.family':'NanumGothicCoding'})

        plt.figure(figsize=(15,15))
        svm = sns.heatmap(data=df.corr(method='pearson'), annot=True, fmt='.2f', linewidths=.5, cmap='Blues')
        figure = svm.get_figure()
        figure.savefig(f'datasets/mini/{db_id}_{file_name[:-4]}_Pearson_heatmap.png', dpi=400)

        plt.figure(figsize=(15,15))
        svm = sns.heatmap(data=df.corr(method='spearman'), annot=True, fmt='.2f', linewidths=.5, cmap='Reds')
        figure = svm.get_figure()
        figure.savefig(f'datasets/mini/{db_id}_{file_name[:-4]}_Spearman_heatmap.png', dpi=400)

        plt.figure(figsize=(15,15))
        svm = sns.heatmap(data=df.corr(method='kendall'), annot=True, fmt='.2f', linewidths=.5, cmap='Greens')
        figure = svm.get_figure()
        figure.savefig(f'datasets/mini/{db_id}_{file_name[:-4]}_Kendall_heatmap.png', dpi=400)


 
    except Exception as e:
        raise APIException(ex=e)
    return mini_path


def change_path(path, source, target):
    path = path.replace(source, target)

    return path


def transform_analysis_data(df, pre_data_name, db_id, filename):
    try:
        response = httpx.get(f'http://happycom.icnslab.net:8281/api/sensor-manage')
        response = response.json()


        sensor_dict = {}

        contents = response['data']['content']
        for content in contents:
            ssId = content['ssId']
            ssName = content['ssType']['typeDtl']

            sensor_dict[ssId] = f'{ssName}_{ssId}'


        df['created_at'] = pd.to_datetime(df['created_at'])


        df_wide = pd.pivot_table(df, index=['created_at'], columns='ss_id', values='input_data', aggfunc='mean')


        df_wide = df_wide.reset_index()

        df_wide = df_wide.rename(columns=sensor_dict)
        df_wide.sort_values(by=['created_at'], inplace=True)

        save_csv_data(df_wide, pre_data_name)

        save_mini_data(file_path=pre_data_name, source='pre', target='mini', db_id=db_id, is_origin=True)

        update_pre_status(db_id=db_id, path=pre_data_name, filename=filename, preProcessState=1)

    except Exception as e:
        print(222)
        raise e

    return df, True