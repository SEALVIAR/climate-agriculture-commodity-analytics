import requests #Permite la coenxión con servidores en la web
import pandas as pd #Clasica para el uso de dataset
import unicodedata #Normaliza los caracteres unicode es decir que elimina acentos y caracteres especiales
import re #Se usa para buscar, validar o transformar texto mediante patrones.
import time #Maneja el tiempo y las pausas de ejecución
import os #Interactuar con el sistema operativo
from urllib.parse import quote #Se usa para codificar cadenas en formato URL

COUNTRIES_NO = ['Bahamas','Cape Verde','Congo (Democratic Republic of the)','Congo','Faroe Islands','French Guiana','Guadeloupe','Palestina','Reunion','Serbia',
                'Tanzania''Czech Republic', 'French Polynesia']
COUNTRIES =['Burkina Faso', 'Slovenia', 'Angola', 'Lesotho', 'Mexico', 'Senegal', 'Finland', 'Israel', 'Qatar',  'Zimbabwe',
            'Federated States of Micronesia', 'Norway', 'Dominican Republic', 'Uganda', 'Australia', 'Oman', 'Ghana', 'Austria', 'Morocco',
            'China', 'Germany', 'Bolivia', 'Honduras', 'Bahrain', 'India', 'Mauritius', 'Netherlands', 'Dominica', 'Syria',
             'Tajikistan','Philippines', 'Georgia', 'Tunisia', 'Lebanon', 'Albania', 'Portugal', 'Lithuania',
            'Guinea', 'Egypt', 'Uruguay', 'Guinea-Bissau', 'Belgium', 'Iraq', 'Canada', 'Kuwait', 'Kazakhstan', 'Japan', 'Indonesia', 'Ukraine',
            'Mauritania', 'Croatia', 'Equatorial Guinea', 'Bosnia And Herzegovina', 'Niger', 'Luxembourg',
            'Gambia', 'Romania', 'Central African Republic', 'Zambia', 'Colombia', 'Puerto Rico', 'Cambodia', 'Chad', 'Ecuador', 'Switzerland',
            'Nicaragua', 'Spain', 'Hungary', 'Guyana', 'Fiji', 'Vietnam', 'Djibouti', 'Sri Lanka', 'Greece', 'Jamaica', 'Sudan', 'El Salvador',
            'Malawi', 'Panama', 'Macedonia', 'Russia', 'Montenegro', 'Bangladesh', 'Slovakia', 'Algeria', 'Belize', 'Libya', 'Madagascar', 'Costa Rica',
            'Botswana', 'United Arab Emirates', 'Bhutan', 'United States', 'New Zealand', 'Nigeria', 'Gabon', 'Belarus', 'Barbados', 'Paraguay', 'Malaysia',
            'Jordan', 'Haiti', 'Argentina', 'Mongolia', 'Suriname', 'Cuba', 'South Africa', 'Cameroon', 'Afghanistan', 'Brazil', 'United Kingdom (Europe)',
            'Namibia', 'Ethiopia', 'Burundi', 'Nepal', 'Ireland', 'Eritrea', 'Antigua and Barbuda',  'France', 'Mali', 'Saudi Arabia',
             'Liberia', 'Yemen', 'Venezuela', 'Bulgaria', 'Italy', 'Singapore', 'Thailand', 'Turkey', 'Chile', 'Cyprus', 'Malta', 'Grenada',
            'Somalia', 'Iran', 'Laos', 'Azerbaijan', 'Peru',  'Rwanda', 'Uzbekistan', 'Kyrgyzstan', 'Poland', 'Benin', 'Guatemala',
            'Kenya', 'Mozambique', 'Sweden', 'Armenia', 'Pakistan',  'Denmark (Europe)', 'Estonia']  #Paises a descargar

URL_BASE = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Regional/TAVG/{slug}-TAVG-Trend.txt" #Estructura base del URL

CARPETA_SALIDA = "Datos_berkeley_txt" #Nombre de la carpeta dónde se descargaran los txt
os.makedirs(CARPETA_SALIDA, exist_ok=True) #Crear si no existe


def pais_a_slug(name):
  """
  La función recibe el nombre de un país y lo adapta al slug necesario
  para usar en el URL base
  """
  #Normalización unicode
  nfkd = unicodedata.normalize("NFKD", name) 

  #Eliminar los caracteres que no sean ASCII
  ascii_name = nfkd.encode("ascii", "ignore").decode("ascii") 

  #Convertir a minisculas y reemplazar los espacios
  slug = re.sub(r"\s+", "-", ascii_name.lower())

  #Caracteres especiales en codificación URL
  slug = quote(slug)

  return slug

#Abrir la conexión continua con el servidor
session = requests.Session()

"""
La siguiente parte del script se encarga de tomar la lista con los paises
que queremos descargar, construye la URL y procede a descargar el archivo
"""
#Iterar sobre la lista de los paises
for country in COUNTRIES:
  #Construir el slug
  slug = pais_a_slug(country)

  #Construir el URL
  url = URL_BASE.format(slug=slug)

  #Ruta para guardar el archivo
  filepath = os.path.join(CARPETA_SALIDA, f"{slug}.txt")

  #Si el archivo ya existe no descargar de nuevo
  if os.path.exists(filepath):
    print(f"skip {country}")
    continue

  try:
    #Descargar el archivo del servidor (esperar maximo 20 segundos)
    respuesta = session.get(url, timeout=20)

    #Verificar si fue descargado (200 --> archivo encontrado)
    if respuesta.status_code == 200:
      #Guardar el archivo
      with open(filepath, "wb") as f:
        f.write(respuesta.content)

      print(f"Exitoso: {country}")

    else:
      print(f"Error: {country} ({respuesta.status_code})")

  except Exception as e:

    print(f"ERROR {country}: {e}")

  #Esperar 0.2 segundos para la siguiente solicitud evitando bloqueos
  time.sleep(0.2)
