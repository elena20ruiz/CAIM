"""
.. module:: SearchIndexWeight

SearchIndex
*************

:Description: SearchIndexWeight

    Performs a AND query for a list of words (--query) in the documents of an index (--index)
    You can use word^number to change the importance of a word in the match

    --nhits changes the number of documents to retrieve

:Authors: bejar


:Version:

:Created on: 04/07/2017 10:56

"""
from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

import argparse

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q

__author__ = 'bejar'


"""
FUNCIONS LABS ANTERIORS
"""

def normalize(tw):
    """
    Normalizes the weights in t so that they form a unit-length vector
    It is assumed that not all weights are 0
    :param tw:
    :return:
    """
    suma = 0
    for _,x in tw:
        suma += x
    return [float(w)/suma for _,w in tw]

def toTFIDF(client, index, file_id):
    """
    Returns the term weights of a document
    :param file:
    :return:
    """
    # Get document terms frequency and overall terms document frequency
    file_tv, file_df = document_term_vector(client, index, file_id)
    max_freq = max([f for _, f in file_tv])
    dcount = doc_count(client, index)

    tfidfw = []
    for (t, w),(_, df) in zip(file_tv, file_df):
        # 1. Calculo tfid: nombre freq del doc entre freq total
        tfid = w / max_freq
        # 2. Calculo idfi (inversa freq del doc sobre el term i)
        idfi = math.log(dcount / df,2)
        weight = tfid * idfi
        tfidfw.append([t,weight])
        pass
    return normalize(tfidfw)

def RocchioRule(alpha,query,beta,mean):
    """
    NOU CODI
    Aplica la regla de Rocchio aplicant els parametres d'entrada
    """
    #1.Transformar query en diccionari amb pesos
    dquery = {}
    for word in query:
        if "^" not in word:
            dquery.append(word,1)
        else:
            s = word.split("^")
            dquery.append([s[0],s[1]])

    #2. Calcular nous pesos
    newquery= {}
    for q in dquery:
        w = alpha*q + beta*mean
        newquery.append([q.key,w])

    #TODO: 3. Passar un altre cop de diccionari a query
    newq = ""
    for nq in newquery:
        newq.join(nq[0],"^",nq[1]," ")
    return newq



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, help='Index to search')
    parser.add_argument('--nhits', default=10, type=int, help='Number of hits to return')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')
    parser.add_argument('--nrounds', default=1, type=int, help='Rounds for applicate Rocchio formula')
    parser.add_argument('-R', default=None, type=int, help='The maximum number of new terms to be kept in the new query')
    parser.add_argument('--alpha', default=None, type=int, help='Alpha weight to a Rocchio rule')
    parser.add_argument('--beta', default=None, type=int, help='Beta weight to a Rocchio rule')
    args = parser.parse_args()

    index = args.index
    query = args.query
    print(query)
    nhits = args.nhits
    """
    NOU CODI: Noves entrades
    """
    nrounds = args.nrounds
    r = args.r
    alpha = args.alpha
    beta = args.beta

    try:
        client = Elasticsearch()
        s = Search(using=client, index=index)

        if query is not None:
            #FIRST ITERATION: NO ROCCHIO RULE
            q = Q('query_string',query=query[0])
            for i in range(1, len(query)):
                q &= Q('query_string',query=query[i])

            s = s.query(q)
            docsit = s[0:nhits].execute()
            #START NEW ROUNDS APPLYIN ROCCHIO RULE
            for i in range(0,nrounds):
                #TODO: Calcular MEAN a partir de docsit

                q = RocchioRule(alpha,q,beta,mean)  #Retornem nova query
                #EXECUTEM PER A LA SEGÜENT ITERACIÓ
                s = s.query(q)
                docsit = s[0:nhits].execute()

            #ORDEN FINAL
            response = s[0:nhits].execute()
            for r in response:  # only returns a specific number of results
                print('ID= %s SCORE=%s' % (r.meta.id,  r.meta.score))
                print('PATH= %s' % r.path)
                print('TEXT: %s' % r.text[:50])
                print('-----------------------------------------------------------------')
        else:
            print('No query parameters passed')

        print ('%d Documents'% response.hits.total)

    except NotFoundError:
        print('Index %s does not exists' % index)
