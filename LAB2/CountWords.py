"""
.. module:: CountWords

CountWords
*************

:Description: CountWords

    Generates a list with the counts and the words in the 'text' field of the documents in an index

:Authors: bejar


:Version:

:Created on: 04/07/2017 11:58

"""

from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from elasticsearch.exceptions import NotFoundError

import argparse

__author__ = 'bejar'

# Convention: returns true if should be removed, based on criteria
def contains_numbers(s):
    return any(char.isdigit() for char in s)

def contains_dots(s):
    return any(char == '.' for char in s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=True, help='Index to search')
    parser.add_argument('--alpha', action='store_true', default=False, help='Sort words alphabetically')
    args = parser.parse_args()

    index = args.index

    try:
        client = Elasticsearch()
        voc = {}
        sc = scan(client, index=index, doc_type='document', query={"query" : {"match_all": {}}})
        for s in sc:
            tv = client.termvectors(index=index, doc_type='document', id=s['_id'], fields=['text'])
            if 'text' in tv['term_vectors']:
                for t in tv['term_vectors']['text']['terms']:
                    if t in voc:
                        voc[t] += tv['term_vectors']['text']['terms'][t]['term_freq']
                    else:
                        voc[t] = tv['term_vectors']['text']['terms'][t]['term_freq']

        lpal = []

        for v in voc:
            if not (v == int) :
                    lpal.append((v.encode("utf8", "ignore"), voc[v]))

        results = {}
        for pal, cnt in sorted(lpal, key=lambda x: x[0 if args.alpha else 1]):
            #Es guarda per a cada paraula cuants cops esta
            results[pal] = cnt
        sortedWords = sorted(results, key=results.get, reverse = True)
        for v in sortedWords:
            print('%d, %s' % (results[v], v))
        print('%s Words' % len(lpal))
        suma=0
        for l in sortedWords:
            suma += int(results[l])
        print('%s Words total' % suma)
    except NotFoundError:
        print('Index %s does not exists' % index)
