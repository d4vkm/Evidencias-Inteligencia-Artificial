import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

#nltk.download('stopwords')

# Define el conjunto de stopwords en inglés
stopwords = set(stopwords.words('english'))

#carga el conjunto de datos:
datos = pd.read_csv('/workspaces/Evidencias-Inteligencia-Artificial/Unidad 2/Tarea 3/spam_assassin.csv/spam_assassin.csv')

#preprocesa los datos:
datos["text"] = datos["text"].str.lower()
datos["text"] = datos["text"].str.replace("[^a-zA-Z0-9 ]"," ")
datos["text"] = datos["text"].str.split()
datos["text"] = datos["text"].apply(lambda x: " ".join([word for word in x if word not in stopwords]))

#extrae características:
vectorizador = TfidfVectorizer(stop_words="english")
features = vectorizador.fit_transform(datos["text"])

#calcula la probabilidad previa de spam:
pSpam = datos["target"].sum() / len(datos)

#calcula la probabilidad previa de no spam:
pNoSpam = 1 - pSpam

#calcula la probabilidad de las características del correo dado que es spam:
pCaracteristicasSpam = features[datos["target"] == 1].sum(axis=0) / features[datos["target"] == 1].sum()

#calcula la probabilidad de las características del correo dado que no es spam:
pCaracteristicasNoSpam = features[datos["target"] == 0].sum(axis=0) / features[datos["target"] == 0].sum()

#calcula la propabilidad posterior de que el correo sea spam:
pSpamCaracteristicas = (pSpam * pCaracteristicasSpam) / (pSpam * pCaracteristicasSpam + pNoSpam * pCaracteristicasNoSpam)

#clasifica:
clasificaciones = np.where(pSpamCaracteristicas > 0.5, "spam", "no spam")

#evalua:
precision = np.sum(clasificaciones == datos["target"]) / len(clasificaciones)
recuperacion = np.sum(clasificaciones == datos["target"]) / datos["target"].sum()

print("Precision: ", precision)
print("Recuperación: ", recuperacion)