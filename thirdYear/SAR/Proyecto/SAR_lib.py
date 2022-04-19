"""
Grupo 3CO11
Miembros: 
     Bernabéu Pérez, Pablo 
     Bou Betran, Santiago 
     Glennie England, Liam James 
     Santolaria Leiva, Guillermo 

Funcionalidades Extra Implementadas:
    Stemming
    Multifield
    Ranking
    Funcionalidad Conjunta
"""


import json
from nltk.stem.snowball import SnowballStemmer
import os
import re
import math

class SAR_Project:
    """
    Prototipo de la clase para realizar la indexacion y la recuperacion de noticias
        
        Preparada para todas las ampliaciones:
          parentesis + multiples indices + posicionales + stemming + permuterm + ranking de resultado

    Se deben completar los metodos que se indica.
    Se pueden añadir nuevas variables y nuevos metodos
    Los metodos que se añadan se deberan documentar en el codigo y explicar en la memoria
    """

    # lista de campos, el booleano indica si se debe tokenizar el campo
    # NECESARIO PARA LA AMPLIACION MULTIFIELD
    fields = [("title", True), ("date", False),
              ("keywords", True), ("article", True),
              ("summary", True)]
    
    
    # numero maximo de documento a mostrar cuando self.show_all es False
    SHOW_MAX = 10


    def __init__(self):
        """
        Constructor de la classe SAR_Indexer.
        NECESARIO PARA LA VERSION MINIMA

        Incluye todas las variables necesaria para todas las ampliaciones.
        Puedes añadir más variables si las necesitas 

        """
        self.index = {} # hash para el indice invertido de terminos --> clave: termino, valor: posting list.
                        # Si se hace la implementacion multifield, se pude hacer un segundo nivel de hashing de tal forma que:
                        # self.index['title'] seria el indice invertido del campo 'title'.
        self.sindex = {} # hash para el indice invertido de stems --> clave: stem, valor: lista con los terminos que tienen ese stem
        self.ptindex = {} # hash para el indice permuterm.
        self.docs = {} # diccionario de documentos --> clave: entero(docid),  valor: ruta del fichero.
        self.weight = {} # hash de terminos para el pesado, ranking de resultados. puede no utilizarse {"article":{"token": [(newsId, Ocurrencias), ...]}, "title":{}}
        self.news = {} # hash de noticias --> clave entero (newsid), valor: la info necesaria para diferenciar la noticia dentro de su fichero (doc_id y posición dentro del documento)
        self.tokenizer = re.compile("\W+") # expresion regular para hacer la tokenizacion
        self.stemmer = SnowballStemmer('spanish') # stemmer en castellano
        self.show_all = False # valor por defecto, se cambia con self.set_showall()
        self.show_snippet = False # valor por defecto, se cambia con self.set_snippet()
        self.use_stemming = False # valor por defecto, se cambia con self.set_stemming()
        self.use_ranking = False  # valor por defecto, se cambia con self.set_ranking()

        # Variables Adicionales

        # Inicializar el contador de indices a 0 para su uso en diferentes llamadas a la función
        self.lastDoc  = -1
        self.lastNews = -1

    ###############################
    ###                         ###
    ###      CONFIGURACION      ###
    ###                         ###
    ###############################


    def set_showall(self, v):
        """

        Cambia el modo de mostrar los resultados.
        
        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_all es True se mostraran todos los resultados el lugar de un maximo de self.SHOW_MAX, no aplicable a la opcion -C

        """
        self.show_all = v


    def set_snippet(self, v):
        """

        Cambia el modo de mostrar snippet.
        
        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_snippet es True se mostrara un snippet de cada noticia, no aplicable a la opcion -C

        """
        self.show_snippet = v


    def set_stemming(self, v):
        """

        Cambia el modo de stemming por defecto.
        
        input: "v" booleano.

        UTIL PARA LA VERSION CON STEMMING

        si self.use_stemming es True las consultas se resolveran aplicando stemming por defecto.

        """
        self.use_stemming = v


    def set_ranking(self, v):
        """

        Cambia el modo de ranking por defecto.
        
        input: "v" booleano.

        UTIL PARA LA VERSION CON RANKING DE NOTICIAS

        si self.use_ranking es True las consultas se mostraran ordenadas, no aplicable a la opcion -C

        """
        self.use_ranking = v




    ###############################
    ###                         ###
    ###   PARTE 1: INDEXACION   ###
    ###                         ###
    ###############################


    def index_dir(self, root, **args):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        
        Recorre recursivamente el directorio "root" e indexa su contenido
        los argumentos adicionales "**args" solo son necesarios para las funcionalidades ampliadas

        """

        self.multifield = args['multifield']
        self.positional = args['positional']
        self.set_stemming(args['stem'])
        self.permuterm = args['permuterm']

        for dir, subdirs, files in os.walk(root):
            for filename in files:
                if filename.endswith('.json'):
                    fullname = os.path.join(dir, filename)
                    self.index_file(fullname)

        ##########################################
        ## COMPLETAR PARA FUNCIONALIDADES EXTRA ##
        ##########################################

        if (self.use_stemming):
            self.make_stemming()

    def index_file(self, filename):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Indexa el contenido de un fichero.

        Para tokenizar la noticia se debe llamar a "self.tokenize"

        Dependiendo del valor de "self.multifield" y "self.positional" se debe ampliar el indexado.
        En estos casos, se recomienda crear nuevos metodos para hacer mas sencilla la implementacion

        input: "filename" es el nombre de un fichero en formato JSON Arrays (https://www.w3schools.com/js/js_json_arrays.asp).
                Una vez parseado con json.load tendremos una lista de diccionarios, cada diccionario se corresponde a una noticia

        """
        # Incrementar contador de ultimo Id
        self.lastDoc += 1
        # Añadir el documento a la lista global
        self.docs[self.lastDoc] = filename 

        with open(filename) as fh:
            jlist = json.load(fh)

        # "jlist" es una lista con tantos elementos como noticias hay en el fichero,
        # cada noticia es un diccionario con los campos:
        #      "title", "date", "keywords", "article", "summary"
        #
        # En la version basica solo se debe indexar el contenido "article"

            for pos, piece in enumerate(jlist):
                # Incrementar contador de ultimo Id de News
                self.lastNews += 1
                # Añadir el article a la lista global de noticias con 
                # el doc en el que aparece y su posición dentro de la misma
                self.news[self.lastNews] = [self.lastDoc, pos]
                
                # Unicamente indexar todos los campos si la flag multifield está activada
                fieldsList = self.fields if self.multifield else [("article", True)]

                for tipo, tokenizar in fieldsList:
                        
                    content = piece[tipo]
                    # Si no se debe tokenizar el campo, se convierte en una lista con 
                    # un único elemento sobre el que se itera para sacar los tokens
                    tokens = self.tokenize(content) if tokenizar else [content]
                    
                    # Primer nivel del diccionario, se crea una entrada para cada campo
                    entryField = self.index.setdefault(tipo, {})

                    # Para el diccionario de pesos, se inicializa una entrada por cada campo
                    entryWeightField = self.weight.setdefault(tipo, {})

                    for token in tokens:
                        # Si el token no tiene una entrada en el diccionario, se crea una nueva
                        entry = entryField.setdefault(token, [])
                        # Por cada token, se crea una entrada nueva si no existe
                        entryWeight = entryWeightField.setdefault(token, {})
                        # Si el identificador de la noticia no está en la posting list, lo añadimos
                        if self.lastNews not in entry:
                            entry.append(self.lastNews)
                            entryWeight[self.lastNews] = 1
                        else:
                            # Si la entrada para el token ya existía en el diccionario, se incrementa
                            # el contador para la noticia actual
                            entryWeight[self.lastNews] += 1



    def tokenize(self, text):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Tokeniza la cadena "texto" eliminando simbolos no alfanumericos y dividientola por espacios.
        Puedes utilizar la expresion regular 'self.tokenizer'.

        params: 'text': texto a tokenizar

        return: lista de tokens

        """
        return self.tokenizer.sub(' ', text.lower()).split()



    def make_stemming(self):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING.

        Crea el indice de stemming (self.sindex) para los terminos de todos los indices.

        self.stemmer.stem(token) devuelve el stem del token

        """
        for field, dictCampo in self.index.items(): 
            # Para cada field, creamos una entrada en la lista de indices de stems
            entry = self.sindex.setdefault(field, {})
            # Comprobar si el campo actual debe ser tokenizado según la lista fields
            if [v[1] for v in self.fields if v[0] == field][0]: 
                for token in dictCampo:
                    # Si el stem del token no tiene una entrada en el diccionario, se crea una nueva
                    entryField = entry.setdefault(self.stemmer.stem(token), [])
                    # Si el token del stem no esta en la lista de tokens, lo añadimos
                    if token not in entryField:
                        entryField.append(token)
            else:
                # Para el caso que el campo no deba ser tokenizado, iteramos el diccionario original
                for token in dictCampo:
                    # Creamos una entrada en el diccionario de stems para cada elemento del campo no tokenizable, 
                    # tal que la clave y el valor sean iguales y se correspondan a dicho elemento
                    entryField = self.sindex[field].setdefault(token,[])
                    if token not in entryField:
                        entryField.append(token)




    def make_permuterm(self):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM

        Crea el indice permuterm (self.ptindex) para los terminos de todos los indices.

        """
        pass
        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################




    def show_stats(self):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        
        Muestra estadisticas de los indices
        
        """
        
        print("=" * 20)
        print("Number of indexed days: " + str(self.lastDoc + 1))
        print("-" * 20)
        print("Number of indexed news: " + str(self.lastNews + 1))
        print("-" * 20)
        print("TOKENS: ")
        if self.multifield:
            print("\t# of tokens in 'title': " + str(len(self.index["title"].keys())))
            print("\t# of tokens in 'date': " + str(len(self.index["date"].keys())))
            print("\t# of tokens in 'keywords': " + str(len(self.index["keywords"].keys())))
            print("\t# of tokens in 'article': " + str(len(self.index["article"].keys())))
            print("\t# of tokens in 'summary': " + str(len(self.index["summary"].keys())))
        else:
            print("\t# of tokens in 'article': " + str(len(self.index["article"].keys())))

        print("-" * 20)
        if (self.use_stemming):
            print("STEMS: ")
            if self.multifield:
                print("\t# of tokens in 'title': " + str(len(self.sindex["title"].keys())))
                print("\t# of tokens in 'date': " + str(len(self.sindex["date"].keys())))
                print("\t# of tokens in 'keywords': " + str(len(self.sindex["keywords"].keys())))
                print("\t# of tokens in 'article': " + str(len(self.sindex["article"].keys())))
                print("\t# of tokens in 'summary': " + str(len(self.sindex["summary"].keys())))
            else:
                print("\t# of tokens in 'article': " + str(len(self.sindex["article"].keys())))
            
            print("-" * 20)

        print("Positional queries are" + (" " if self.positional else " NOT ") + "allowed.")
        print("=" * 20)


    ###################################
    ###                             ###
    ###   PARTE 2.1: RECUPERACION   ###
    ###                             ###
    ###################################


    def solve_query(self, query, prev={}):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una query.
        Debe realizar el parsing de consulta que sera mas o menos complicado en funcion de la ampliacion que se implementen


        param:  "query": cadena con la query
                "prev": incluido por si se quiere hacer una version recursiva. No es necesario utilizarlo.


        return: posting list con el resultado de la query

        """
        if len(query) == 0 and len(prev) > 0:
            return prev

        if query is None or len(query) == 0:
            return []

    
    ###############################################


        if type(query) is str:
            tokens = query.split(" ")
            
        else:
            tokens = query
        # Cogemos la primera word de la query
        word = tokens[0]
        # Si la primera palabra es un OR o AND, comprobamos si la siguiente es un NOT
        if word in ["AND", "OR"]:
            nextword = tokens[1]
            # Si la siguiente palabra es un NOT, obtendremos la posting list invertida del segundo termino
            if nextword == "NOT":
                # Obtenemos el field para el término en caso de que exista
                wordField = self.get_field(tokens[2])
                if word == "AND":
                    prev = self.and_posting(prev, self.reverse_posting(self.get_posting(wordField[0], wordField[1]))) 
                else:
                    prev = self.or_posting(prev, self.reverse_posting(self.get_posting(wordField[0], wordField[1])))
                # Llamamos recursivamente a partir de la siguiente palabra que no hemos analizado todavía
                return self.solve_query(tokens[3:], prev)
            # Si la siguiente palabra no es un NOT, haremos la operacion normal
            else:
                # Obtenemos el field para el término en caso de que exista
                wordField = self.get_field(nextword)
                if word == "AND":
                    prev = self.and_posting(prev, self.get_posting(wordField[0], wordField[1])) 
                else:
                    prev = self.or_posting(prev, self.get_posting(wordField[0], wordField[1]))
                return self.solve_query(tokens[2:], prev)
        # Si la primera palabra es un NOT, obtendremos la posting list invertida (solo cuando la query original empieza por NOT)
        elif word == "NOT":
            # Obtenemos el field para el término en caso de que exista
            wordField = self.get_field(tokens[1])
            prev = self.reverse_posting(self.get_posting(wordField[0], wordField[1]))
            return self.solve_query(tokens[2:], prev)
        # Si la primera palabra es un término, se obtiene la posting list del termino (solo cuando la query original empieza con un termino)
        else:
            # Obtenemos el field para el término en caso de que exista
            wordField = self.get_field(word)
            prev = self.get_posting(wordField[0], wordField[1])
            return self.solve_query(tokens[1:], prev)

    def get_field(self, term):
        """
            PARA IMPLEMENTACION MULTIFIELDS
            Separa y devuelve una lista con el field y el campo 
            incluido en un término para ejecutar consultas multifield.
        """

        if (':' in term):
            res = term.split(':')
            res.reverse()
            return res
        return [term, 'article']
        
    def get_posting(self, term, field='article'):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Devuelve la posting list asociada a un termino. 
        Dependiendo de las ampliaciones implementadas "get_posting" puede llamar a:
            - self.get_positionals: para la ampliacion de posicionales
            - self.get_permuterm: para la ampliacion de permuterms
            - self.get_stemming: para la amplaicion de stemming


        param:  "term": termino del que se debe recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """
        # Para realizar busquedas tras normalizar los tokens, usamos el termino de la query en minusculas
        # Esto se debe a que almacenamos la posting list con los token en minúsculas
        term = term.lower()
        
        if self.use_stemming:
            return self.get_stemming(term, field)

        if term not in self.index[field]:
            return []

        return self.index[field][term]



    def get_positionals(self, terms, field='article'):
        """

        NECESARIO PARA LA AMPLIACION DE POSICIONALES

        Devuelve la posting list asociada a una secuencia de terminos consecutivos.

        param:  "terms": lista con los terminos consecutivos para recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """
        pass
        ########################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE POSICIONALES ##
        ########################################################


    def get_stemming(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING

        Devuelve la posting list asociada al stem de un termino.

        param:  "term": termino para recuperar la posting list de su stem.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """
        # Si el campo es de tipo tokenizable, se realiza el stemming del token
        # Si no lo es, el token se mantiene inalterado
        if [v[1] for v in self.fields if v[0] == field][0]:
            stem = self.stemmer.stem(term)
        else:
            stem = term

        res= []
        if stem not in self.sindex[field]:
            return []
            
        for word in self.sindex[field][stem]:
            for newsId in self.index[field][word]:
                if newsId not in res:
                    res.append(newsId)
        # Al insertar las posting list de palabras diferentes se deja de cumplir el orden de las noticias
        # Para que algoritmos como el AND o el OR funcionen se debe ordenar la posting list.
        res.sort()
        return res



    def get_permuterm(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM

        Devuelve la posting list asociada a un termino utilizando el indice permuterm.

        param:  "term": termino para recuperar la posting list, "term" incluye un comodin (* o ?).
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """

        ##################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA PERMUTERM ##
        ##################################################




    def reverse_posting(self, p):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Devuelve una posting list con todas las noticias excepto las contenidas en p.
        Util para resolver las queries con NOT.


        param:  "p": posting list


        return: posting list con todos los newsid excepto los contenidos en p

        """
        res = []
        for index in self.news.keys():
            if index not in p:
                res.append(index)
        return res


    def and_posting(self, p1, p2):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Calcula el AND de dos posting list de forma EFICIENTE

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newsid incluidos en p1 y p2

        """
        
        res = []
        pos1 = pos2 = 0
        while pos1 < len(p1) and pos2 < len(p2):
            w1 = p1[pos1]
            w2 = p2[pos2]
            if w1 == w2:
                res.append(w1)
                pos1 += 1
                pos2 += 1
            elif w1 < w2:
                pos1 += 1
            else:
                pos2 += 1
        return res



    def or_posting(self, p1, p2):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Calcula el OR de dos posting list de forma EFICIENTE

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newsid incluidos de p1 o p2

        """

        res = []
        pos1 = pos2 = 0
        while pos1 < len(p1) and pos2 < len(p2):
            w1 = p1[pos1]
            w2 = p2[pos2]
            # Si ambos elementos son iguales, se añade uno de los elementos y se avanzan ambos punteros
            if w1 == w2:
                res.append(w1)
                pos1 += 1
                pos2 += 1
            # Si son distintos, añadimos el que tiene la posición menor y esta se adelanta
            elif w1 < w2:
                res.append(w1)
                pos1 += 1
            else:
                res.append(w2)
                pos2 += 1
 
        # Al llegar al final de alguna de las listas, 
        # copiamos todos los elementos restantes de la otra lista al resultado
        while pos1 < len(p1):
            w1 = p1[pos1]
            res.append(w1)
            pos1 += 1

        while pos2 < len(p2):
            w2 = p2[pos2]
            res.append(w2)
            pos2 += 1
        return res


    def minus_posting(self, p1, p2):
        """
        OPCIONAL PARA TODAS LAS VERSIONES

        Calcula el except de dos posting list de forma EFICIENTE.
        Esta funcion se propone por si os es util, no es necesario utilizarla.

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newsid incluidos de p1 y no en p2

        """

        
        pass
        ########################################################
        ## COMPLETAR PARA TODAS LAS VERSIONES SI ES NECESARIO ##
        ########################################################





    #####################################
    ###                               ###
    ### PARTE 2.2: MOSTRAR RESULTADOS ###
    ###                               ###
    #####################################


    def solve_and_count(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una consulta y la muestra junto al numero de resultados 

        param:  "query": query que se debe resolver.

        return: el numero de noticias recuperadas, para la opcion -T

        """
        result = self.solve_query(query)
        print("%s\t%d" % (query, len(result)))
        return len(result)  # para verificar los resultados (op: -T)


    def solve_and_show(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una consulta y la muestra informacion de las noticias recuperadas.
        Consideraciones:

        - En funcion del valor de "self.show_snippet" se mostrara una informacion u otra.
        - Si se implementa la opcion de ranking y en funcion del valor de self.use_ranking debera llamar a self.rank_result

        param:  "query": query que se debe resolver.

        return: el numero de noticias recuperadas, para la opcion -T
        
        """
        result = self.solve_query(query)
        if self.use_ranking and len(result) != 0:
            result = self.rank_result(result, query)   
        else:
            # En caso que no utilizemos score, se establece en 0 para todos los artículos
            result = [(news,0) for news in result]
            
        
        print("=" * 20)
        print("Query: " + query)
        print("Number of results: " + str(len(result)))

        
        for posResult, [curNew, score] in enumerate(result):
            print("#"+str(posResult+1))

            # score = self.rank_result(result, query) if self.use_ranking else 0
            print("Score: %.4f" % score)

            # Se imprime el id de la noticia
            print(curNew)

            [docId, posInDoc] = self.news[curNew]

            with open(self.docs[docId]) as curDoc:
                article = json.load(curDoc)[posInDoc]

                print("Date: " + article["date"])
                print("Title: " + article["title"])
                print("Keywords: " + article["keywords"])
                # Implementación: Snippet de cada término
                if self.show_snippet:
                    articulo = self.tokenize(article["article"])
                    # Eliminamos "article:" al buscar el snippet para hacer el resumen
                    consulta = query.replace("article:", "").split(" ")
                    if self.use_stemming:
                        # En el caso de que se use stemming, devolver el snippet con el stem de la palabra buscada en mayúsculas
                        for pos, q in enumerate(consulta):
                            consulta[pos] = self.stemmer.stem(q)
                        positions = []
                        for posSnippet, word in enumerate(articulo):
                            sword = self.stemmer.stem(word) 
                            if sword in consulta:
                                consulta.remove(sword)
                                positions.append(posSnippet)
                        res = ""
                        for posSnippet in positions:
                            # Unimos las 5 palabras anteriores con la palabra de la consulta en mayúsculas y las 5 posteriores
                            foundWord = articulo[posSnippet]
                            foundWordStem = self.stemmer.stem(foundWord).upper()
                            foundWord = foundWordStem + foundWord[len(foundWordStem):]
                            res += " ".join(articulo[max(0, posSnippet-5):posSnippet] + [foundWord] + articulo[posSnippet+1: min(posSnippet+6, len(articulo))]) + "... "
                    else:
                        # En el caso de que no se use stemming, devolver el snippet con la palabra buscada en mayúsculas
                        positions = []
                        for posSnippet, word in enumerate(articulo):
                            if word in consulta:
                                consulta.remove(word)
                                positions.append(posSnippet)
                        res = ""
                        for posSnippet in positions:
                            # Unimos las 5 palabras anteriores con la palabra de la consulta en mayúsculas y las 5 posteriores
                            res += " ".join(articulo[max(0, posSnippet-5):posSnippet] + [articulo[posSnippet].upper()] + articulo[posSnippet+1: min(posSnippet+6, len(articulo))]) + "... "
                    print(res)

            print("-" * 10)
            if not self.show_all and posResult+1 >= self.SHOW_MAX:
                break

        print("=" * 20)

        return len(result)  # para verificar los resultados (op: -T)




    def rank_result(self, result, query):
        """
        NECESARIO PARA LA AMPLIACION DE RANKING

        Ordena los resultados de una query.

        param:  "result": lista de resultados sin ordenar
                "query": query, puede ser la query original, la query procesada o una lista de terminos


        return: la lista de resultados ordenada, formada por tuplas (newsId, score)

        """

        # Se extraen los términos relevantes dentro de la query para el cálculo del rank
        tokens = [token for token in query.split(" ") if token not in ["AND", "OR"]]
        terminos = []
        for i in range(0, len(tokens)):
            if tokens[i] == "NOT":
                i += 1
            else:
                terminos.append(tokens[i].lower())
                
        #ltc.ltc
        # Noticias: log-pesado, idf y coseno normalizado
        # Query: log-pesado, idf y coseno normalizado
        # Score = Suma del producto por término para cada noticia
        
        # Obtenemos el field de cada termino
        terminosField = [self.get_field(term) for term in terminos]

        # En caso de utilizar stemming, calcular el rank en base a los stems
        if self.use_stemming:
            for pos, [term, field] in enumerate(terminosField):
                terminosField[pos] = [self.stemmer.stem(term), field]

        #Calculamos el Score para cada término en la consulta
        queryScore = {}
        # Almacenamos el idf para evitar su cálculo posterior
        idf = {}
        for [term, field] in terminosField:
            # Obtener la frecuencia del término en la consulta
            sumaFreq = sum([1 for [termSearch, _] in terminosField if term == termSearch])
            # Formula:  tf    = 1 + log(freqTermEnDoc)
            tf = 1 + math.log(sumaFreq, 10)    
            # Formula: idf   = log(Ndocs/numDocConTerm)
            # En caso de usar stemming, es necesario sumar las ocurrencias en todos los documentos de los términos con el mismo stem
            if self.use_stemming:
                sumaFreqStem = 0
                for derivedTerm in self.sindex[field][term]:
                    if derivedTerm in self.weight[field]:
                        sumaFreqStem += len(self.weight[field][derivedTerm])
                # sumaFreqStem siempre contendrá al menos una ocurrencia dentro de la noticia actual
                # Guardamos el idf para su posterior uso en el cálculo por documento para evitar calculos innecesarios
                idf[term] = math.log(len(self.news)/sumaFreqStem, 10)
            else:
                idf[term] = math.log(len(self.news)/len(self.weight[field][term]), 10)  
            # Formula: w[i]  = tf*idf
            queryScore[term] = tf*idf[term] 
        
        # Formula: lNorm = w[i]/sqrt(sum(w^2))
        sumQueryScore = math.sqrt(sum(v * v for v in queryScore.values()))
            

        for term in queryScore.keys():
            # Si todos los términos suman 0, el score de todos los documentos será 0
            if sumQueryScore == 0:
                queryScore[term] = 0
            else:
                queryScore[term] /= sumQueryScore

        ranking = []  
        for news in result:
            newsScore = {}
            for [term, field] in terminosField:
                # Formula: tf    = 1 + log(freqTermEnDoc)
                sumaFreq = 0
                if self.use_stemming:
                    # Para cada término derivado del stem, acumulamos el número de aparciciones de cada término en la noticia
                    for derivedTerm in self.sindex[field][term]:
                        if derivedTerm in self.weight[field] and news in self.weight[field][derivedTerm]:
                            sumaFreq += self.weight[field][derivedTerm][news]
                else:
                    # Numero de apariciones del término en la noticia
                    sumaFreq = self.weight[field][term][news]
                tf = 1 + math.log(sumaFreq, 10)
                # w[i]  = tf*idf (el idf se ha calculado previamente)
                newsScore[term] = tf*idf[term]
            # lNorm = w[i]/sqrt(sum(w^2))
            sumNewsScore = math.sqrt(sum(v * v for v in queryScore.values()))
            for term in newsScore.keys():
                # Si todos los términos suman 0, el score de todos los documentos será 0
                if sumNewsScore == 0:
                    newsScore[term] = 0
                else:
                    newsScore[term] /= sumNewsScore
            # Calculo del coseno entre la query y el documento actual (newsId) 
            # cos(q, newsId) = suma(scoreQuery + scoreNewsId) para cada término
            newsScoreValue = sum([newsScore[term] * queryScore[term] for term in newsScore.keys()])
            ranking.append((news, newsScoreValue))
        
        ranking.sort(reverse=True, key=lambda x:x[1])

        return ranking
        
    