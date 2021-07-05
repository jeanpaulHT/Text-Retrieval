# Text-Retrieval
literalmente el segundo proyecto de bd-II
## Integrantes

- Esteban Villacorta  201910336
- Jean Paul Huby Tuesta 201910194
- Daniela Abril Vento Bustamante 201910331

## Descripción

El objetivo del proyecto será la implementación de un motor buscador de tweets usando índice invertido para la consulta de una gran cantidad de tweets de manera eficiente usando lenguaje natural como input de la consulta. 


# Recolección de data y procesamiento de la data

Para la recolección de tweets se uso la API **snscrape**. Se optó por esta API debido a que la API ofrecida por Twitter **tweepy**, tiene limitaciones respecto a la cantidad de tweets que se pueden buscar y el tiempo de respuesta. Solo se estan aceptando tweets de lenguaje español y que sean tweets originales (no se aceptan retweets sin texto) los cuales se dividen en distintos archivos, cada archivo teniendo una cantidad máxima de tweets.

Todo esto es hecho en el archivo `fastTracker.py`. El resultado de la busqueda se guardará en `texts/raw`

Estos archivos son tratados por separado desde el preprocesamiento hasta la creación del index, en donde se aplicará el *Blocked Sort-Based Indexing* para usar de manera mas eficiente el espacio del RAM. Todo esto sera explicado a detalle en las siguientes secciones. 

# Implementacion

## Preprocesamiento

Antes de la creación del index invertido, se tienen que proprocesar los contenidos de cada tweet. Esto implica eliminar términos que se consideren de poca relevancia, tales como signos o palabras que son muy poco informativas como para ser relevantes. Los signos que se remueven estan definidos en `skipped_symbols` y las palabras estan definidas en `stop_list`

A cada palabra que quede después del filtro, se le aplica el proceso de stemming. Este proceso tiene el objetivo de dejar solo la raíz de las palabras para considerar palabras similares como el mismo término y mejorar la búsqueda de una query. Se usa la librería **nltk** para esto.

El preprocesamiento funciona por etapas:
1) **preprocess_file**: extrae la información del tweet y escribe el resultado de las otras 2 etapas.
2) **parse_line**:  se encarga de extraer las palabras o símbolos inválidos.
3) **preprocess_text**: una última verificación de las palabras y se ejecuta el proceso de stemming.

Los resultados del preprocesamiento se guardan en `texts/preprocessing`.

## Índice invertido

Para calcular el resultado score de un query se propuso una estructura de índice invertido que reduzca el número de operaciones que necesarias para obtener el resultado del score.

El índice invertido consiste de un término I el cual tiene como calores un **idf**, relacionado con el término el cual es calculado al momento de la construcción. El otro valor que es guardado es un **post_list**, el cual consiste guarda un tupla que guarda el documento donde aparece el término y el número de ocurrencias de ese término en el documento. 

index:
```
t0-> [idf , post_list[(docID , tf)] , ...]
t1-> [idf , post_list[(docID , tf)] , ...]
.
.
tn -> [idf , post_list[(docID , tf)] , ...]
```
Para no tener que calcular la norma cada vez que se hace un query, esta se guarda en un file distinto del cual puede ser extraido al momento del cálculo del score.

norm:
```
Doc0: norm0
.
.
DocI: normI
```


## Manejo de memoria secundaria

Como no se puede leer todos los índices de todos los archivos a la vez, creamos inicialmente bloques pequeños, que denominamos **MergeableIndex**, que contienen la data separadamente. Estos índices luego pueden ser combinados utilizando la función `MergeableIndex.merge`. Este proceso de merge se realiza hasta que solo quede un índice final. 

Inicialmente, se utilizan los files generados por el preprocessor para generar los MergeableIndex iniciales. Luego, se agregan todos los índices parciales a una lista. Para cada par de elementos adyacentes, se llama a merge y se genera un upper level index. Una vez que ya no quedan más indices que no puedan ser mergeados, se reemplaza la lista por la nueva capa. Esto se repite hasta que solo quede el índice final. Asumiendo que existan `N` índices iniciales (bloques) de tamaño `B`, el índice final se reconstruye en `O(N * B * lg(N))`.

El procedimiento puede verse en la siguiente imagen:

![alt text](https://github.com/jeanpaulHT/Text-Retrieval/blob/main/bd-diagram.png)


## Tiempos de ejecución
Para una cantidad de tweets igual a:  20 000

- Preprocessing: 18.16 segundos
- Recoleccion de tweets: 5 minutos
- Tiempos de ejecución:
    - 0.05 segundos (caso promedio)
    - 3.2714511 segundos (peor caso)



# Requisitos

- Flask 
- python3
- snscrape
- nltk

## Pruebas de uso y presentación

- [Vídeo del proyecto](https://drive.google.com/drive/folders/1vCWJYOEFpJduP1AZBpRjJouA5BNZIWBy?usp=sharing)

