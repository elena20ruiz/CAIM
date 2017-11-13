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

import argparse

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.client import CatClient
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q

__author__ = 'bejar'

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



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, help='Index to search')
    parser.add_argument('--nhits', default=10, type=int, help='Number of hits to return')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')

    args = parser.parse_args()

    index = args.index
    query = args.query
    print(query)
    nhits = args.nhits

    try:
        client = Elasticsearch()
        s = Search(using=client, index=index)

        #PARTE SIN ROCCIO
        if query is not None:
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
