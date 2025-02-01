import requests
import csv
from bs4 import BeautifulSoup

def realizar_scraping(url):
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.content, 'html.parser')

        enlaces_horoscopo = soup.find_all('a', class_='story-item__title', href=True)
        enlaces_filtrados = [enlace['href'] for enlace in enlaces_horoscopo if "horoscopo-de-hoy" in enlace['href'] and "vivo" not in enlace['href']]
        
        if enlaces_filtrados:
            return enlaces_filtrados
        else:
            return "No se encontraron enlaces del horóscopo."

    else:
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
                texto = siguiente_parrafo.get_text()
                predicciones_horoscopo.append(texto)

        return signos_horoscopo, predicciones_horoscopo

    else:
        return f"Error al acceder a la página: {respuesta.status_code}"

url = 'https://elcomercio.pe/noticias/horoscopo/'
enlaces = realizar_scraping(url)

with open('horoscopo.csv', mode='w', newline='', encoding='utf-8') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerow(['Signo', 'Predicciones'])  # Escribir encabezados

    for enlace in enlaces[:1]:
        signos, predicciones = obtener_contenido_horoscopo("https://elcomercio.pe" + enlace)
        for signo, prediccion in zip(signos, predicciones):
            escritor_csv.writerow([signo, prediccion])  # Escribir datos en el CSV