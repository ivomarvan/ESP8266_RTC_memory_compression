#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"
__description__ = '''
    Vrátí entropii pro jednotlivé sloupce

    Inputs:
        - vstupní adresář s *.csv
    
'''

import sys
import os.path
import pandas as pd
from pprint import pprint
import numpy as np
from math import log2 as log2

# root of lib repository
PROJECT_ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../..')
DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')
sys.path.append(PROJECT_ROOT)

class DataEntropy:

    def __init__(
        self,
        infile,
        outfile
    ):
        self.infile = infile
        self.outfile = outfile


    def run(self):
        # načti
        df = pd.read_csv(self.infile.name, sep='\t', header=0, index_col=False, na_values=None)
        totalEntropy = 0
        for colName in df.columns:
            # normuj
            df[colName] = df[colName] + -min(df[colName]) + 1
            df[colName] = df[colName].fillna(0)
            entropy = self.entropy2(list(df[colName]))
            print(colName, entropy)
            totalEntropy += entropy
        l = len(df);
        print('celkem průměrně bitů na jsedno měření [bit]', totalEntropy)
        print('počet měření', l)
        print('déka při kódování [bit]', l*totalEntropy)
        print('déka při kódování [byte]', int(l * totalEntropy/8 +1))



    def entropy2(self, labels):
        """ Computes entropy of label distribution. """
        n_labels = len(labels)

        if n_labels <= 1:
            return 0

        counts = np.bincount(labels)
        probs = counts / n_labels
        n_classes = np.count_nonzero(probs)

        if n_classes <= 1:
            return 0

        ent = 0.

        # Compute shannon entropy.
        for pi in probs:
            if pi > 0:

                ent -= pi * log2(pi)

        return ent

# --- Spustitelná část programu ----------------------------------------------------------------------------------------

if __name__ == '__main__':
    import argparse
    from py.lib.cmdLine.processor import Processor
    from py.lib.cmdLine.cmdLineParser import CmdLineParser

    class Program(Processor, CmdLineParser):
        '''
        Spouštěcí část skriptu. Command line, Exceptions, ...
        '''

        def __init__(self):
            # zpracuje příkazovou řádku
            CmdLineParser.__init__(self, description=__description__)

            # spustí program, zachytí výjimky
            Processor.__init__(self)


        def _addArgsToCmdLineParser(self, parser):
            '''
            Definice příkazové řádky
            '''

            default = os.path.join(os.path.expanduser(DATA_ROOT), 'energomonitor/f2_W.time.dif.tsv')
            #default = os.path.join(os.path.expanduser(DATA_ROOT), 'energomonitor/1000.tsv.gz')
            parser.add_argument(
                '-i', '--input-file',
                dest='infile',
                metavar='<infile>',
                type=argparse.FileType('r'),
                help='Vstupní tsv soubor se všemi naměřenými daty (default:' + default + ')',
                default=default,
                required=False
            )

            default =  os.path.join(os.path.expanduser(DATA_ROOT), 'energomonitor/f2_W.time.dif.ent.tsv')
            parser.add_argument(
                '-o', '--output-file',
                dest='outfile',
                metavar='<outfile>',
                type=argparse.FileType('w'),
                help='Výstubní png s obrázkem (default:' + str(default) + ')',
                default=default,
                required=False
            )

        def run(self):
            DataEntropy(
                infile=self.cmdLineParams.infile,
                outfile=self.cmdLineParams.outfile
            ).run()


    Program()


