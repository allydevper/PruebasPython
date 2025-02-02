import pandas as pd
import re

# Cargar el dataset
datos = pd.read_csv('web_scraping/test.csv')

# Verificar que no haya valores nulos
print(datos.isnull().sum())

def limpiar_texto(texto):
    # Eliminar caracteres especiales y números
    texto = re.sub(r'[^a-zA-ZáéíóúñÁÉÍÓÚÑ\s]', '', texto)
    # Convertir a minúsculas
    texto = texto.lower()
    return texto

datos['Contenido'] = datos['Contenido'].apply(limpiar_texto)

from sklearn.feature_extraction.text import TfidfVectorizer

# Vectorizar el texto usando TF-IDF
vectorizer = TfidfVectorizer(max_features=1000)  # Limitar a 1000 palabras más frecuentes
X = vectorizer.fit_transform(datos['Contenido'])
y = datos['Signo']  # Etiquetas (signos del zodiaco)

from sklearn.model_selection import train_test_split

# Dividir los datos: 80% entrenamiento, 20% prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Entrenar el modelo
modelo = MultinomialNB()
modelo.fit(X_train, y_train)

# Evaluar el modelo
y_pred = modelo.predict(X_test)
print(f'Precisión: {accuracy_score(y_test, y_pred)}')
print(classification_report(y_test, y_pred))