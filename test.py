import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from gensim.models import Word2Vec
from imblearn.over_sampling import SMOTE
import nltk
import numpy as np

# Descargar recursos de NLTK
nltk.download('stopwords')

# Leer los datos
datos = pd.read_csv('web_scraping/test.csv')

# Inicializar herramientas de procesamiento de texto
stop_words = set(stopwords.words('spanish'))
stemmer = SnowballStemmer('spanish')

# Preprocesamiento del texto
def limpiar_texto(texto):
    texto = re.sub(r'[^a-zA-ZáéíóúñÁÉÍÓÚÑ\s]', '', texto)  # Quitar caracteres especiales
    texto = texto.lower()  # Convertir a minúsculas
    texto = ' '.join([stemmer.stem(palabra) for palabra in texto.split() if palabra not in stop_words])  # Stemming y stopwords
    return texto

datos['Contenido'] = datos['Contenido'].apply(limpiar_texto)

# Entrenar un modelo Word2Vec con Gensim
oraciones = [texto.split() for texto in datos['Contenido']]
modelo_word2vec = Word2Vec(sentences=oraciones, vector_size=300, window=5, min_count=1, workers=4)

# Generar embeddings usando Word2Vec
def generar_embedding(texto):
    palabras = texto.split()
    if len(palabras) == 0:  # Manejar el caso de textos vacíos
        return np.zeros(300)
    vector = np.mean([modelo_word2vec.wv[palabra] for palabra in palabras if palabra in modelo_word2vec.wv] or [np.zeros(300)], axis=0)
    return vector

# Generar los embeddings para cada texto
embeddings = datos['Contenido'].apply(generar_embedding)
X = pd.DataFrame(embeddings.tolist())  # Convertir a DataFrame para manipular
y = datos['Signo']

# Balancear clases con SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled)

# Entrenar modelo Random Forest
modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_rf.fit(X_train, y_train)

# Evaluar modelo
y_pred = modelo_rf.predict(X_test)
print(f'Precisión: {accuracy_score(y_test, y_pred)}')
print(classification_report(y_test, y_pred))
