#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"
__description__ = '''
    Načte TSV soubor a zapíše variantu s poslední známým rozdílem.

    Inputs:
        - vstupní tsv soubor

    Výstup:
        - výstupní tsv soubor
'''

import sys
import os.path
import pandas as pd
from pprint import pprint
import csv

# root of lib repository
PROJECT_ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../..')
DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')
sys.path.append(PROJECT_ROOT)

class DataDiff:

    def __init__(
        self,
        infile,
        outfile
    ):
        self.infile = infile
        self.outfile = outfile


    def run(self):
        # načti
        reader = csv.reader(self.infile, delimiter='\t')
        writer = csv.writer(self.outfile, delimiter='\t')
        lastValues = [0] * 3
        minValues = [sys.maxsize] *3
        maxValues = [-sys.maxsize] * 3
        for i, row in enumerate(reader):
            if not i:
                # prní řádek
                writer.writerow(row)
            else:
                for j,value in enumerate(row):
                    if value == '':
                        continue;
                    value = int(float(value))
                    diff = value - lastValues[j]
                    minValues[j] = min(minValues[j], diff)
                    maxValues[j] = max(maxValues[j], diff)
                    lastValues[j] = value
                    row[j] = diff
                writer.writerow(row);
        for j, value in enumerate(minValues):
            print(j, 'min=', minValues[j])
            print(j, 'max=', maxValues[j])


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

            default = os.path.join(os.path.expanduser(DATA_ROOT), 'energomonitor/f2_W.time.tsv')
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

            default =  os.path.join(os.path.expanduser(DATA_ROOT), 'energomonitor/f2_W.time.dif.tsv')
            parser.add_argument(
                '-o', '--output-file',
                dest='outfile',
                metavar='<outfile>',
                type=argparse.FileType('w'),
                help='Výstubní tsv soubor s výsledky (default:' + str(default) + ')',
                default=default,
                required=False
            )

        def run(self):
            DataDiff(
                infile=self.cmdLineParams.infile,
                outfile=self.cmdLineParams.outfile
            ).run()


    Program()


