from fastapi import Request

from app.models.exceptions import *
from app.internal.utils import *
from app.internal.restAPI import *

import pandas as pd
import math

from statsmodels.tsa.api import VAR


def interpolate(data, columns, pre_data_root_directory, data_name, db_id):
    try:


        processed_columns = []
        processed_data = {}

        origin_columns = data.columns

        for origin_column in origin_columns:
            processed_columns.append(origin_column)
            origin_column_data = data[origin_column]

            if origin_column in columns:
                processed_column_data = origin_column_data.interpolate(method='values', limit_direction='both')
                processed_data[origin_column] = processed_column_data
            else:
                processed_data[origin_column] = origin_column_data

        df = pd.DataFrame(processed_data, columns=processed_columns)

        pre_data_path = f'{pre_data_root_directory}/{data_name}'

        save_csv_data(df, pre_data_path)
        save_path = save_mini_data(pre_data_path, source='pre', target='mini', db_id=db_id)

        pre_data_path = pre_data_path.replace('./', '')

        r = update_pre_status(db_id, f'{pre_data_path}', data_name, 1)
        
    except Exception as e:
        print(222)
        raise e

    return df, True



def pearson(data, columns, pre_data_root_directory, data_name, db_id):
    try:
  
        ar = 10
        pearson_dict = {}
        result_column = []
        result_data = {}

        columns = ['load', 'year']
        origin_data = data
        origin_columns = origin_data.columns

        null_index_dict = {}
        for name in origin_columns:
            li = list(origin_data[name][origin_data[name].isnull()].index)
            if (len(li) != 0):
                null_index_dict[name] = li

        fillna_origin_data = origin_data.fillna(method="ffill")
        fillna_origin_data = origin_data.fillna(method="bfill")

        res_df = origin_data.copy()

        for column in columns:
            result_column.append(column)

            pearson_dict[column] = {}
            for origin_column in origin_columns:
                try:
                    pearson_cor = pearsonr(fillna_origin_data[column], fillna_origin_data[origin_column])[0]
                    if math.isnan(pearson_cor) != True:
                        pearson_dict[column][origin_column] = pearson_cor

                except Exception as e:
                    pearson_dict[column][origin_column] = -1
                    pass
            pearson_dict[column] = sorted(pearson_dict[column].items(), key = lambda item: item[1], reverse=True)

            processed_data = {}
            processed_columns = []

            processed_columns.append(column)
            processed_data[column] = fillna_origin_data[column]

            # todo: pearson 중요도 처리
            for pearson_column in pearson_dict[column]:
                # todo: 시간 데이터 처리
                if pearson_column[0] == column or pearson_column[0] == 'date':
                    continue
                processed_columns.append(pearson_column[0])
                processed_data[pearson_column[0]] = fillna_origin_data[pearson_column[0]]

            df = pd.DataFrame(processed_data, columns=processed_columns)

            try:
                forecasting_model = VAR(df)
                results = forecasting_model.fit(ar)


            except Exception as e:
                raise APIException(ex=e)

            try:
                for idx in null_index_dict[column]:
                    y = df.values[idx-ar:idx]
                    if idx-ar < 0:
                        res_df.loc[idx, column] = round(fillna_origin_data.loc[res_df.loc[idx, column], column], 3)
                    else:
                        forecast_res = pd.DataFrame(results.forecast(y=y, steps=1), columns=processed_columns)
                        res_df.loc[idx, column] = round(float(forecast_res[column].iloc[0]), 3)

            except:
                res_df[column] = fillna_origin_data[column]
                pass
            
        pre_data_path = f'{pre_data_root_directory}/{data_name}'

        save_csv_data(res_df, pre_data_path)
        save_path = save_mini_data(pre_data_path, source='pre', target='mini', db_id=db_id)


        pre_data_path = pre_data_path.replace('./', '')
        r = update_pre_status(db_id, f'{pre_data_path}', data_name, 1)

    except Exception as e:
        raise APIException(ex=e)

    return True