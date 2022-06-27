import requests, os, logging
from  cfg import date_file, date_folder, MUSEOS_URL, CINES_URL, BIBLIOTECAS_URL

logging.basicConfig(level='DEBUG')

# Se crean las carpetas si no existen
categories = ['bibliotecas', 'cines', 'museos', 'results']
for category in categories:
    try:
        os.mkdir(f'boards/{category}/{date_folder}')
    except :
        pass

# Guardado de los archivos
try:
    with requests.get(MUSEOS_URL) as r:
        with open(f"boards/museos/{date_folder}/museos-{date_file}.csv", "wb") as f:
            f.write(r.content)
    with requests.get(CINES_URL) as r:
        with open(f"boards/cines/{date_folder}/cines-{date_file}.csv", "wb") as f:
            f.write(r.content)
    with requests.get(BIBLIOTECAS_URL) as r:
        with open(f"boards/bibliotecas/{date_folder}/bibliotecas-{date_file}.csv", "wb") as f:
            f.write(r.content)
    logging.info('Data downloaded successfully')
except Exception as e:
    logger.error(f'Data download has not been completed, exception: {e}')