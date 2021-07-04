# Text-Retrieval
literalmente el segundo proyecto de bd-II
## Integrantes

- Esteban Villacorta  201910336
- Jean Paul Huby Tuesta 201910194
- Daniela Abril Vento Bustamante 201910331

## Descripción

El objetivo del proyecto sera la implementacion de un motor buscador  de tweets usando indice invertido para la consulta de una gran cantidad de tweets de manera eficiente usando lenguaje natural como input de la consulta. 


# Recoleccion de data y procesamiento de la data

Para la recoleccion de tweets se uso la api snscrape para recolectar tweeter, solo se esta aceptando tweets de lengauje español y que sean tweets originales (no se aceptan retweets)  los cuales se dividen en distintos archivos. Cada archivo teniendo una cantidad de tweets maximo.

Todo esto es hecho en el archivo `fastTracker.py`. Cabe decir que esta implementacion para recolectar tweets hace uso del api **snscrape** debido a las limitaciones que el api ofrecido por twiiter **tweepy** viene con una gran cantidad de limitaciones con respecto a la cantidad de tweets buscado y el tiempo de respuesto. la implementacion con snacrape nos libera de estas limitaciones.  Sin embargo si se quiere hacer una busqueda mas exhaustiva y el tiempo no es una limitacion se recomiendo la implementacion de `tracker.py`. El resultado de la busqueda se guardara en `texts/raw`

Estos archivos son tratados por separado hasta desde el preprocesamiento hasta la creacion del index, en donde se aplicara el Blocked Sort-Based Indexing para usar de manera mas eficiente el espacio del ram. Todo esto sera explicado a detalle en las siguintes secciones. 

# Implementacion

## Preprocesamiento

Antex de la creacion del index invertido se tiene que proprocesar los contenidos que cada tweets. Esto sirve para eliminar terminos que se consideren de poca relevancia. Tales como signos o palabras que son muy poco informativas como para ser relevantes. Los signos que se remueven estan definidos en  `skipped_symbols` y las palabras estan definidas en `stop_list`

Cada palabras que se quede despues del filtro se le aplica el proceso de steaming. Con el objetivo para quedarnos con la raiz de las palabras para mejorar para considerar palabras similares como el mismo termino, para mejorar la busqueda de una query. Se usa la libreria **nltk** para esto.

El preprocesamiento funciona por etapas:
1) **preprocess_file**: extrae la informacion del tweet y escribe el resultado de las otras 2 etapas
2) **parse_line**:  se encarga de extraer las palabras o simbolos invalidos
3) **preprocess_text**: una ultima verifacion de las palabras y se ejecuta el proceso de stemming 

los resultados del preprocesamiento se guardan en `texts/preprocessing`.

## Indice invertido

Para calcular el resultado score de un query se propuso una estructura de indice invertido que reduzca el numero de operaciones que necesarias para obtener el resultado del score.

el inverted index consiste de un termino I el cual tiene como calores un **idf** relacionado con el termino el cual es calculado al momento de construccion. El otro valor que es guardado es un **post_list** el cual consiste guarda un tupla que guarda el documento donde aparece el termino y el numero de ocurrencias de ese termino en el documento. 

index:
```
t0-> [idf , post_list[(docID , tf)] , ...]
t1-> [idf , post_list[(docID , tf)] , ...]
.
.
tn -> [idf , post_list[(docID , tf)] , ...]
```
Para no tener que calcular la norma cada vez que se hace un query, esta se guarda en un file distinto del cual puede ser extraido al momento del calculo del score.

norm:
```
Doc0: norm0
.
.
DocI: normI
```


## Manejo de memoria secundaria



## Tiempos de ejecucion


# Requisitos

- Flask 
- python3
- snscrape
- nltk

## Pruebas de uso y presentación

- [Explicación del proyecto]()
- [Pruebas funcionales]()

