import pandas
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from textblob import TextBlob
import csv

def leerDataset():
    #Carga el dataset de entrenamiento:
    with open('/workspaces/Evidencias-Inteligencia-Artificial/Unidad 2/Tarea 3/SMSSpamCollection') as smsSpamCollection:
        datasetDeEntrenamiento = [line.strip() for line in smsSpamCollection]
        print(f"El dataset de entrenamiento tiene {len(datasetDeEntrenamiento)} registros")

    datos = pandas.read_csv('/workspaces/Evidencias-Inteligencia-Artificial/Unidad 2/Tarea 3/SMSSpamCollection',
                               sep='\t',
                               quoting=csv.QUOTE_NONE,
                               names=['class','message'])

    #Imprime los primeros 5 registros:
    print(datos.head())

    #Los clasifica:
    print(datos.groupby('class').count())

    return datos

def formatearPalabras(palabrasDelMensaje):
    mensaje = str(palabrasDelMensaje).lower()
    palabrasLematizadas= TextBlob(mensaje).words
    return [palabra.lemma for palabra in palabrasLematizadas]

datos = leerDataset()

vectorDeEntrenamiento=CountVectorizer(analyzer=formatearPalabras).fit(datos.get('message'))

#message10 = vectorDeEntrenamiento.transform([datos.get('message')[9]])

#print(message10)

#bolsa de palabras de todo el dataset:
bolsaDePalabras = vectorDeEntrenamiento.fit_transform(datos.get('message').values)

#cantidad por palabra (frecuencia por término y frecuencia inversa):
mensajesTfIdf = TfidfTransformer().fit(bolsaDePalabras).transform(bolsaDePalabras)

#entrenar el modelo:
detectorDeSpam=MultinomialNB().fit(mensajesTfIdf, datos.get('class').values)

#Prueba:
ejemplo=['FREE CASH $$$ click here for more information']

resultado = detectorDeSpam.predict(vectorDeEntrenamiento.transform(ejemplo))[0]

print(f'El mensaje "{ejemplo[0]}" es {resultado}')