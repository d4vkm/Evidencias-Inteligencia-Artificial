import pandas
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from textblob import TextBlob
import csv

def leerDataset():
    #Carga el dataset de entrenamiento:
    with open('/workspaces/Evidencias-Inteligencia-Artificial/Unidad 2/Tarea 3/spam_assassin.csv/spam_assassin.csv') as spamAssassin:
        datasetDeEntrenamiento = [line.strip() for line in spamAssassin]
        print(f"El dataset de entrenamiento tiene {len(datasetDeEntrenamiento)} registros")

    datos = [line.rsplit(',', 1) for line in datasetDeEntrenamiento]
    df = pandas.DataFrame(datos, columns=["text", "target"])
    df = df.drop(index=0)

    #df["target"] = pandas.to_numeric(df["target"])

    #Imprime los primeros 5 registros:
    print(df.head())

    #Los clasifica:
    print(df.groupby('target').count())

    return df

def formatearPalabras(palabrasDelMensaje):
    mensaje = str(palabrasDelMensaje).lower()
    palabrasLematizadas= TextBlob(mensaje).words
    return [palabra.lemma for palabra in palabrasLematizadas]

datos = leerDataset()

vectorDeEntrenamiento=CountVectorizer(analyzer=formatearPalabras).fit(datos.get('text'))

#message10 = vectorDeEntrenamiento.transform([datos.get('message')[9]])

#print(message10)

#bolsa de palabras de todo el dataset:
bolsaDePalabras = vectorDeEntrenamiento.fit_transform(datos.get('text').values)

#cantidad por palabra (frecuencia por término y frecuencia inversa):
mensajesTfIdf = TfidfTransformer().fit(bolsaDePalabras).transform(bolsaDePalabras)

#entrenar el modelo:
detectorDeSpam=MultinomialNB().fit(mensajesTfIdf, datos.get('target').values)

#Prueba:
ejemplo=['FREE CASH $$$ click here for more information']
ejemplo2=['hi dude, how are you?']

resultado = detectorDeSpam.predict(vectorDeEntrenamiento.transform(ejemplo2))[0]

print(f'El mensaje "{ejemplo2[0]}" es {resultado}')