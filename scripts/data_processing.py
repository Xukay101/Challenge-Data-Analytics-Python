import pandas as pd, logging
from cfg import date_file, date_folder

logging.basicConfig(level='DEBUG')
# Creacion de nueva tabla normalizada
columns = [
        'cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia', 'localidad', 'nombre', 'domicilio', 'codigo postal', 'telefono', 'mail', 'web', 'fuente'
]
df_united_data = pd.DataFrame(columns=columns)

logging.info('Opening csv files')
# Abrir datos extraidos
try:
    df_museos = pd.read_csv(f'boards/museos/{date_folder}/museos-{date_file}.csv')
    df_cines = pd.read_csv(f'boards/cines/{date_folder}/cines-{date_file}.csv')
    df_bibliotecas = pd.read_csv(f'boards/bibliotecas/{date_folder}/bibliotecas-{date_file}.csv')
except:
    logging.error('The files could not be opened')
    exit()

logging.info('Processing and renaming data')
#  Renombrar nombres de las columnas
for category in [df_museos, df_bibliotecas, df_cines]:
    category.rename(
        columns = {
            'Cod_Loc' : columns[0], 'IdProvincia' : columns[1], 'IdDepartamento' : columns[2], 'Categoría' : columns[3],
            'Provincia' : columns[4], 'Localidad' : columns[5], 'Nombre' : columns[6], 'CP' : columns[8],
            'Teléfono' : columns[9], 'Mail' : columns[10], 'Web' : columns[11], 'Fuente' : columns[12]
        }, inplace = True
    )
df_museos.rename(columns = {'direccion' :columns[7]}, inplace = True)
df_bibliotecas.rename(columns = {'Domicilio' : columns[7]}, inplace = True)
df_cines.rename(columns = {'Dirección' : columns[7]}, inplace = True)

# Concatenar las tablas en una sola
df_united_data = pd.concat([df_united_data, df_museos[columns], df_cines[columns], df_bibliotecas[columns]])

# Procesar y unir los registros
df_category = df_united_data.value_counts('categoria').reset_index(name='Cantidad de registros totales por categoria')
df_source = df_united_data.value_counts('fuente').reset_index(name='Cantidad de registros totales por fuente')
df_prov = df_united_data.value_counts(['provincia', 'categoria']).reset_index(name='Cantidad de registros por provincia y categoría')

df_records = df_category.merge(df_source, how='outer', left_index = True, right_index = True).merge(df_prov, how='outer', left_index = True, right_index = True)

# Procesar la informacion de cines por condicion de provincia
df_records2 = df_cines[['provincia', 'Pantallas', 'Butacas']].groupby(['provincia']).sum()
df_records2 = df_records2.merge(df_cines[['provincia', 'espacio_INCAA']].groupby(['provincia']).count(), on='provincia')

# Guardar las tablas en la carpeta resultados
df_united_data.to_csv(f'boards/results/{date_folder}/datos_unidos.csv')
df_records.to_csv(f'boards/results/{date_folder}/registros_totales.csv')
df_records2.to_csv(f'boards/results/{date_folder}/registros_cines.csv')
logging.info('files processed successfully')