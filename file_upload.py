# import needed libraries
from sqlalchemy import create_engine
import pandas as pd
import os

# get password from environment var
pwd = os.environ['PGPASS']
uid = os.environ['PGUID']
server = "localhost"
db = "AdventureWorks"
port = "5432"
dir = r'C:\\Users\\Mads\\Downloads\\Flat Files'

# extract data from excel files
def extract():
    try:
        directory = dir
        # iterate over files in the directory
        for filename in os.listdir(directory):
            file_wo_ext = os.path.splitext(filename)[0]
            # only process excel files
            if filename.endswith(".xlsx"):
                f = os.path.join(directory, filename)
                if os.path.isfile(f):
                    df = pd.read_excel(f)
                    # call load function
                    load(df, file_wo_ext)
    except Exception as e:
        print("Data extract error: " + str(e))

# load data to postgres
def load(df, tbl):
    try:
        rows_imported = 0
        engine = create_engine(f'postgresql://{uid}:{pwd}@{server}:{port}/{db}')
        print(f'importing rows {rows_imported} to {rows_imported + len(df)}... ')
        
        # force lowercase table name to avoid needing quotes in SQL
        table_name = tbl.lower()
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        rows_imported += len(df)
        print(f"Data imported successfully into table: {table_name}")
    except Exception as e:
        print("Data load error: " + str(e))

# main script
try:
    extract()
except Exception as e:
    print("Error while extracting data: " + str(e))
