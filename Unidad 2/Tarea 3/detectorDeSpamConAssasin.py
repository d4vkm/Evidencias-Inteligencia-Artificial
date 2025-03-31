import pandas
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from textblob import TextBlob

def leerDataset():
    #Abre el archivo de mensajes y se lee linea por linea:
    with open('/workspaces/Evidencias-Inteligencia-Artificial/Unidad 2/Tarea 3/spam_assassin.csv/spam_assassin.csv') as spamAssassin:
        datasetDeEntrenamiento = [line.strip() for line in spamAssassin]
        print(f"El dataset de entrenamiento tiene {len(datasetDeEntrenamiento)} registros")

    #divide los renglones del archivo en dos a partir de la primera "," desde la derecha:
    datos = [line.rsplit(',', 1) for line in datasetDeEntrenamiento]
    #A partir de los datos crea un dataframe con columnas "text" y "target" y elimina el primer registro:
    df = pandas.DataFrame(datos, columns=["text", "target"])
    df = df.drop(index=0)

    #Imprime los primeros 5 registros del DataFrame:
    print(df.head())

    #Los clasifica:
    print(df.groupby('target').count())

    return df

def formatearPalabras(palabrasDelMensaje):
    #toma un mensaje y lo transforma a minúsculas:
    mensaje = str(palabrasDelMensaje).lower()
    #toma un mensaje y transforma los caracteres que no se encuentren
    #en esos rangos a espacios:
    mensaje = str(palabrasDelMensaje).replace("[^a-zA-Z0-9 ]"," ")
    #divive el mensaje en palabras lematizadas:
    palabrasLematizadas= TextBlob(mensaje).words
    return [palabra.lemma for palabra in palabrasLematizadas]

datos = leerDataset()

#Crea un vector numérico de las palabras en los mensajes con ayuda del método
#formatearPalabras() para analizar cada mensaje:
vectorDeEntrenamiento=CountVectorizer(analyzer=formatearPalabras).fit(datos.get('text'))

mensaje1 = vectorDeEntrenamiento.transform([datos.get('text')[1]])

print(mensaje1)

#convierte cada mensaje en vectores de frecuencias de palabras y las guarda:
bolsaDePalabras = vectorDeEntrenamiento.fit_transform(datos.get('text').values)

#calcula la importancia de las palabras dandole más peso a las menos comunes:
mensajesTfIdf = TfidfTransformer().fit(bolsaDePalabras).transform(bolsaDePalabras)

#entrena el modelo de Naive Bayes con las representaciones TF-IDF de los mensajes
# y los tipos de mensaje 0 y 1:
detectorDeSpam=MultinomialNB().fit(mensajesTfIdf, datos.get('target').values)

#Pruebas:
ejemplo=['FREE CASH $$$ click here for more information']
ejemplo2=['hey dude, how are you?']

#Se tranforman los mensajes con .transform() a una representación compatible con
# el modelo y se mandan para que el modelo prediga si es spam o normal:
resultado = detectorDeSpam.predict(vectorDeEntrenamiento.transform(ejemplo)[0])
resultado2 = detectorDeSpam.predict(vectorDeEntrenamiento.transform(ejemplo2)[0])

print(f'El mensaje "{ejemplo[0]}" es {resultado[0]}')
print(f'El mensaje "{ejemplo2[0]}" es {resultado2[0]}')