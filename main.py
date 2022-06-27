import os, time

# Nombre de cada script
data_extraction = 'data_extraction.py'
data_processing = 'data_processing.py'
db_connection = 'db_connection.py'

# Verificar que sistema operativo  se esta ejecutando y dar permisos de ejecucion en caso de linux
if os.name == 'posix':
    os.system(f'chmod +x scripts/{data_extraction}')
    os.system(f'chmod +x scripts/{data_processing}')
    prefix = 'python3'
elif os.name == 'ce' or os.name == 'nt' or os.name == 'dos':  # Windows no testeado
    prefix = 'python'

# Ejecuta los scripts en orden - se espera a que termine uno para ejecutar el otro
os.system(f'{prefix} scripts/{data_extraction}')
os.system(f'{prefix} scripts/{data_processing}')
os.system(f'{prefix} scripts/{db_connection}')