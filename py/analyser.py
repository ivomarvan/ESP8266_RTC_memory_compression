#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"
__description__ = '''
    - Read data from TSV (tabulator separated file).
    - Lists statistical information about the data.
    - Encodes and decode the data by various methods.
    - Compare diference beatween input original data an encoded and decodet dat (must be same, for testing).
    - Compares the results of coding for the data (Haw differen coding methode is good fot the data).

    Inputs:
        - tsv input file with data

    Výstup:
        - tsv output with results
'''

import sys
import os.path
import pandas as pd
import math


# root of lib repository
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)


class CodingAnalyser:

    def __init__(
        self,
        infile,
        outfile
    ):
        self.infile = infile
        self.outfile = outfile

    def run(self):
        data = pd.read_csv(self.infile, sep='\t', header=0)
        self.witeDataStats(data)

    def witeDataStats(self, data: pd.DataFrame):
        for i, column in enumerate(data.columns):
            if not i:
                self.outfile.write('name')
            self.outfile.write('\t')
            self.outfile.write(column)
        self.outfile.write('\n' + '-' *80 + '\n')
        data.min().to_csv(self.outfile, header=None)
        data.max().to_csv(self.outfile, header=None)



# --- Spustitelná část programu ----------------------------------------------------------------------------------------

if __name__ == '__main__':
    import argparse
    from lib.cmdLine.processor import Processor
    from lib.cmdLine.cmdLineParser import CmdLineParser

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

            default = sys.stdin
            parser.add_argument(
                '-i', '--input-file',
                dest='infile',
                metavar='<infile>',
                type=argparse.FileType('r'),
                help='input tsv file (default:' + str(default) + ')',
                default=default,
                required=False
            )

            default = sys.stdout
            parser.add_argument(
                '-o', '--output-file',
                dest='outfile',
                metavar='<outfile>',
                type=argparse.FileType('w'),
                help='output tsv file with results (default:' + str(default) + ')',
                default=default,
                required=False
            )

        def run(self):
            CodingAnalyser(
                infile=self.cmdLineParams.infile,
                outfile=self.cmdLineParams.outfile
            ).run()


    Program()