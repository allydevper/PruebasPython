import requests
import re
import csv
from bs4 import BeautifulSoup

def realizar_scraping(url):
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.content, 'html.parser')

        enlaces_horoscopo = soup.find_all('a', class_='story-item__title', href=True)
        enlaces_filtrados = [enlace['href'] for enlace in enlaces_horoscopo if "horoscopo-de-hoy" in enlace['href'] and "vivo" not in enlace['href']]
        
        return enlaces_filtrados if enlaces_filtrados else "No se encontraron enlaces del horóscopo."

    return f"Error al acceder a la página: {respuesta.status_code}"

def obtener_contenido_horoscopo(url):
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.content, 'html.parser')

        signos_horoscopos = soup.find_all('h2', class_='story-contents__header')
        signos_horoscopo = [signos_horoscopo.get_text().split(" ")[0] for signos_horoscopo in signos_horoscopos]

        predicciones_horoscopo = []
        for signo in signos_horoscopos:
            siguiente_parrafo = signo.find_next('p', class_='story-contents__font-paragraph')
            if siguiente_parrafo:
                tipos, contenidos = obtener_eventos_horoscopo(siguiente_parrafo.get_text())
                predicciones_horoscopo.append((tipos, contenidos))

        return signos_horoscopo, predicciones_horoscopo

    return f"Error al acceder a la página: {respuesta.status_code}"

def obtener_eventos_horoscopo(linea):
    original = re.split(r"\.", linea)

    grupo_actual = []

    for item in original:
        item_limpio = item.strip()
        if not item_limpio:
            continue
        if ':' in item_limpio:
            grupo_actual.append(item_limpio)
        else:
            grupo_actual[-1] += " " + item_limpio

    tipos = []
    contenidos = []

    for linea in grupo_actual:
        if ':' in linea:
            tipo, contenido = map(str.strip, linea.split(':', 1))
            tipos.append(tipo.capitalize())
            contenidos.append(contenido.capitalize())
    
    return tipos, contenidos

url = 'https://elcomercio.pe/noticias/horoscopo/'
enlaces = realizar_scraping(url)

with open('horoscopo.csv', mode='w', newline='', encoding='utf-8') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerow(['Signo', 'Tipos', 'Contenidos'])  # Escribir encabezados

    for enlace in enlaces[:1]:
        signos, predicciones = obtener_contenido_horoscopo("https://elcomercio.pe" + enlace)
        for signo, (tipos, contenidos) in zip(signos, predicciones):
            for tipo, contenido in zip(tipos, contenidos):
                escritor_csv.writerow([signo, tipo, contenido])  # Escribir datos en el CSV