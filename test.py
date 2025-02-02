import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from imblearn.over_sampling import SMOTE
import nltk

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

# Representación de texto con TF-IDF
vectorizer = TfidfVectorizer(max_features=2000)  # Aumentar características a 2000
X_texto = vectorizer.fit_transform(datos['Contenido'])

# Incorporar la columna "Categoria" como característica adicional
categorias_dummy = pd.get_dummies(datos['Categoria'], prefix='Categoria')
X_texto_df = pd.DataFrame(X_texto.toarray())  # Convertir la matriz sparse a DataFrame
X_texto_df.columns = [str(i) for i in range(X_texto_df.shape[1])]  # Asegurar que los nombres de columnas sean cadenas

X = pd.concat([X_texto_df, categorias_dummy.reset_index(drop=True)], axis=1)

# Asegurar que todas las columnas tengan nombres como cadenas
X.columns = X.columns.astype(str)

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
