import pandas as pd

# Cargar el dataset
datos = pd.read_csv('web_scraping/horoscopo_base.csv')

# Verificar que no haya valores nulos
print(datos.isnull().sum())

# Convertir el texto a minúsculas (opcional)
datos['Contenido'] = datos['Contenido'].str.lower()

