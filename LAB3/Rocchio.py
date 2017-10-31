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
            dquery.append(s[0],s[1])

    #2. Calcular nous pesos
    newquery= {}
    for q in dquery:
        w = alpha*q + beta*mean
        newquery.append(q.key,w)

    #TODO: 3. Passar un altre cop de diccionari a query
    newq = ""
    for nq in newquery:
        newq.join(nq[0],"^",nq[1]," ")
    return newqu



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
            for i in range(0,nrounds):
                #TODO: Calcular MEAN
                query = RocchioRule(alpha,query,beta,mean)  #Retornem nova query
                q = Q('query_string',query=query[0])
                for i in range(1, len(query)):
                    q &= Q('query_string',query=query[i])

                s = s.query(q)
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
