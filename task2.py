import time
import pandas as pd
from google.cloud import bigquery
from concurrent.futures import ThreadPoolExecutor
import itertools
from google.oauth2 import service_account
import gspread
from gspread_dataframe import set_with_dataframe
from pandas import json_normalize

scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive',
        ]
key_path = r'gsp_api.json'
credentials_sheet = service_account.Credentials.from_service_account_file(key_path, scopes=scopes)
credentials = service_account.Credentials.from_service_account_file(key_path)

#Sheets
sheet_id = '1iqcUaKSdomCiKLMID7XqlKv8oEQOqXuSOHHkx0fZQ5k'
client = gspread.authorize(credentials_sheet)
spreadsheet = client.open_by_key(sheet_id)

#Bigquery
client_ = bigquery.Client(credentials=credentials)
dataset_id = 'bigquery-public-data.google_analytics_sample'

def fetch_table_data(table_id):
    sql_query = f"""
    SELECT *
    FROM `{dataset_id}.{table_id}`
    """
    query_job = client_.query(sql_query)
    return query_job.result()

def write_to_sheet(sheet_name, df):
    try:
        spreadsheet.add_worksheet(title=sheet_name, rows=df.shape[0], cols=df.shape[1])
    except Exception as e:
        pass
    worksheet = spreadsheet.worksheet(sheet_name)
    worksheet.clear()
    return set_with_dataframe(worksheet=worksheet, dataframe=df, include_index=False,
                               include_column_header=True, resize=True)



def main():
    tables = client_.list_tables(dataset_id)
    tables = itertools.islice(tables, 1)

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_table_data, table.table_id)
            for table in tables
        ]

        dfs = [future.result() for future in futures]
        df = pd.read_excel('Untitled spreadsheet.xlsx').astype(str)
        df2 = df.copy()
        for rows in dfs:
            for row in rows:
                d = dict(row)
                for i in row:
                    if isinstance(i, list):
                        if len(i) > 0:
                            i = i[0]
                        else:
                            i = ''
                df_ = json_normalize(d, record_prefix='').astype(str)
                df = pd.merge(df, df_, how='outer')

        df = df.drop(columns=[col for col in df.columns if df[col].map(str).map(len).max() > 1000])
        columns_order = df2.columns.tolist()
        reference_df_subset = df[columns_order]
        df = df.reindex(columns=reference_df_subset.columns)

        agregation_1 = df.copy().groupby('device.browser').size().reset_index(name='count')
        agregation_2 = df.copy().groupby('device.operatingSystem').size().reset_index(name='count')
        agregation_3 = df.copy().groupby('geoNetwork.continent').size().reset_index(name='count')
        agregation_4 = df.copy().groupby('geoNetwork.region').size().reset_index(name='count')

        aggregated = [agregation_1, agregation_2, agregation_3, agregation_4]
        Sheets = ['Sheet1', 'Sheet2', 'Sheet3', 'Sheet4']

        futures = [
            executor.submit(write_to_sheet, *params)
            for params in zip(Sheets, aggregated)
        ]
        for future in futures:
            future.result()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(time.time() - start_time)
