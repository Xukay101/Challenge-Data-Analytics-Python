import pandas as pd, logging
from sqlalchemy import create_engine
from decouple import config
from cfg  import date_file, date_folder

logging.basicConfig(level='DEBUG')

# Conexion y guardado de datos
try:
    logging.info('Attempting to connect to the database...')
    pgname = config('NAME')
    pgpassword = config('PASSWORD')
    pghost = config('HOST')
    pgport = config('PORT')
    pgdb = config('DB')

    url =  f'postgresql://{pgname}:{pgpassword}@{pghost}:{pgport}/{pgdb}'

    db = create_engine(url)

    df_united_data = pd.read_csv(f'boards/results/{date_folder}/datos_unidos.csv')
    df_records = pd.read_csv(f'boards/results/{date_folder}/registros_totales.csv')
    df_records2 = pd.read_csv(f'boards/results/{date_folder}/registros_cines.csv')

    df_united_data.to_sql('datos_unidos', con=db, if_exists='replace')
    df_records.to_sql('registros_totales', con=db, if_exists='replace')
    df_records2.to_sql('registros_cines', con=db, if_exists='replace')
    logging.info('Database connection completed')
except:
    logging.error('Unable to connect to the database')
    exit()
loggin.info('Data correctly loaded into the database')