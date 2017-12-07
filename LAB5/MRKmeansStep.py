"""
.. module:: MRKmeansDef

MRKmeansDef
*************

:Description: MRKmeansDef



:Authors: bejar


:Version:

:Created on: 17/07/2017 7:42

"""

from __future__ import division
from mrjob.job import MRJob
from mrjob.step import MRStep
from math import *

__author__ = 'bejar'

class MRKmeansStep(MRJob):
    prototypes = {}

    def jaccard(self, prot, doc):
        """
        Compute here the Jaccard similarity between  a prototype and a document
        prot should be a list of pairs (word, probability)
        doc should be a list of words
        Words must be alphabeticaly ordered

        The result should be always a value in the range [0,1]
        """
        intersection = len(prot.intersection(doc))
        union = len(prot) + len(doc) - len(intersection)
        sim = intersection/float(union)

        return sim

    def configure_options(self):
        """
        Additional configuration flag to get the prototypes files

        :return:
        """
        super(MRKmeansStep, self).configure_options()
        self.add_file_option('--prot')

    def load_data(self):
        """
        Loads the current cluster prototypes

        :return:
        """
        f = open(self.options.prot, 'r')
        for line in f:
            cluster, words = line.split(':')
            cp = []
            for word in words.split():
                cp.append((word.split('+')[0], float(word.split('+')[1])))
            self.prototypes[cluster] = cp

    def assign_prototype(self, _, line):
        """
        This is the mapper it should compute the closest prototype to a document

        Words should be sorted alphabetically in the prototypes and the documents

        This function has to return at list of pairs (prototype_id, document words)

        You can add also more elements to the value element, for example the document_id
        """

        # Each line is a string docid:wor1 word2 ... wordn
        doc, words = line.split(':')
        lwords = words.split()

        #
        # Compute map here
        #
        p = self.jaccard(self.prototypes,lwords)

        sortedwords = sorted(lwords)
        words = ' '.join(sortedwords)
        value = doc + ":" + words

        # Return pair key, value
        yield p, value

    def aggregate_prototype(self, key, values):
        """
        input is cluster and all the documents it has assigned
        Outputs should be at least a pair (cluster, new prototype)

        It should receive a list with all the words of the documents assigned for a cluster

        The value for each word has to be the frequency of the word divided by the number
        of documents assigned to the cluster

        Words are ordered alphabetically but you will have to use an efficient structure to
        compute the frequency of each word

        :param key:
        :param values:
        :return:
        """
        doc = ""
        words = []
        lwords = []
        allwords = []
        #GUARDAR LAS PALABRAS DISTINTAS CON SU YA VALOR CORRESPONDIENTE
        for line in values:
            doc, words = line.split(':')
            lwords = words.split()
            if(len(allwords) > 0):
                allwords = allwords.union(lwords)
            else:
                allwords = lwords

        #CALCULAR TODAS LAS PALABRAS 1 VEZ
        #SE INSERTA EN EL LUGAR CORRESPONDIENTE
        dic = []
        keys = []
        size = len(values)

        #Primera iteracion
        peso = prototypes[allwords[0]]/size
        data = allwords[0],peso
        dic.insert(data)
        keys.insert(peso)

        for w in allwords[1:len(allwords)]:
            peso = prototypes[w]/size
            data = w,peso
            insert(dic, keys, data, keyfunc=lambda x: x[1])

        # Get centroide
        middle = int(allwords/2)
        prot = dic[middle]

        yield cluster, prot

    def steps(self):
        return [MRStep(mapper_init=self.load_data, mapper=self.assign_prototype,
                       reducer=self.aggregate_prototype)
            ]


if __name__ == '__main__':
    MRKmeansStep.run()
