import pandas as pd

# Cargar el dataset
datos = pd.read_csv('web_scraping/horoscopo_base.csv')

# Verificar que no haya valores nulos
print(datos.isnull().sum())

# Convertir el texto a minúsculas (opcional)
datos['Contenido'] = datos['Contenido'].str.lower()

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