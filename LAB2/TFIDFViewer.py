"""
.. module:: TFIDFViewer

TFIDFViewer
******

:Description: TFIDFViewer

    Receives two paths of files to compare (the paths have to be the ones used when indexing the files)

:Authors:
    bejar

:Version:

:Date:  05/07/2017
"""

from __future__ import print_function, division
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.client import CatClient
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from scipy import spatial
import numpy as np

import math

import argparse

import numpy as np

__author__ = 'bejar'

def search_file_by_path(client, index, path):
    """
    Search for a file using its path

    :param path:
    :return:
    """
    s = Search(using=client, index=index)
    q = Q('match', path=path)  # exact search in the path field
    s = s.query(q)
    result = s.execute()

    lfiles = [r for r in result]
    if len(lfiles) == 0:
        raise NameError('File [%s] not found'%path)
    else:
        return lfiles[0].meta.id


def document_term_vector(client, index, id):
    """
    Returns the term vector of a document and its statistics a two sorted list of pairs (word, count)
    The first one is the frequency of the term in the document, the second one is the number of documents
    that contain the term

    :param client:
    :param index:
    :param id:
    :return:
    """
    termvector = client.termvectors(index=index, doc_type='document', id=id, fields=['text'],
                                    positions=False, term_statistics=True)

    file_td = {}
    file_df = {}

    if 'text' in termvector['term_vectors']:
        for t in termvector['term_vectors']['text']['terms']:
            file_td[t] = termvector['term_vectors']['text']['terms'][t]['term_freq']
            file_df[t] = termvector['term_vectors']['text']['terms'][t]['doc_freq']
    return sorted(file_td.items()), sorted(file_df.items())


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
        " NEW CODI"
        # 1. Calculo tfid
        # nombre freq del doc entre freq total
        tfid = w / max_freq
        # 2. Calculo idfi (inversa freq del doc sobre el term i)
        idfi = math.log(dcount / df,2)
        # 3. Calculo final
        weight = tfid * idfi
        tfidfw.append([t,weight])
        pass

    return normalize(tfidfw)

def print_term_weigth_vector(twv):
    """
    Prints the term vector and the correspondig weights
    :param twv:
    :return:
    """
    "NEW CODI"
    for t,w in twv:
        print('%d,%s' % (w,t))
    pass


def normalize(tw):
    """
    Normalizes the weights in t so that they form a unit-length vector
    It is assumed that not all weights are 0
    :param tw:
    :return:
    """
	"NEW CODI"
    suma = 0
    for _,x in tw:
        suma += x

    return [float(w)/suma for _,w in tw]


def cosine_similarity(tw1, tw2):
    """
    Computes the cosine similarity between two weight vectors, terms are alphabetically ordered
    :param tw1:
    :param tw2:
    :return:
    """
    "NEW CODI"
    if len(tw1) > len(tw2):
        dot_product = np.dot(tw1[0:(len(tw2)-1)], tw2[0:(len(tw2)-1)])
    else:
        dot_product = np.dot(tw1[1:(len(tw1)-1)], tw2[1:(len(tw1)-1)])

    norm_a = np.linalg.norm(tw1)
    norm_b = np.linalg.norm(tw2)
    return dot_product / (norm_a * norm_b)

def doc_count(client, index):
    """
    Returns the number of documents in an index

    :param client:
    :param index:
    :return:
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=True, help='Index to search')
    parser.add_argument('--files', default=None, required=True, nargs=2, help='Paths of the files to compare')
    parser.add_argument('--print', default=False, action='store_true', help='Print TFIDF vectors')

    args = parser.parse_args()


    index = args.index

    file1 = args.files[0]
    file2 = args.files[1]

    client = Elasticsearch()

    try:

        file1_id = search_file_by_path(client, index, file1)
        file2_id = search_file_by_path(client, index, file2)
        file1_tw = toTFIDF(client, index, file1_id)
        file2_tw = toTFIDF(client, index, file2_id)

        if args.print:
            print('TFIDF FILE %s' % file1)
            print_term_weigth_vector(file1_tw)
            print ('---------------------')
            print('TFIDF FILE %s' % file2)
            print_term_weigth_vector(file2_tw)
            print ('---------------------')

        print("Similarity = %3.5f" % cosine_similarity(file1_tw, file2_tw))

    except NotFoundError:
        print('Index %s does not exists' % index)
