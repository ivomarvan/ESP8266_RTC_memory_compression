#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"
__description__ = '''
    Zobrazí (uloží graf).

    Inputs:
        - vstupní adresář s *.csv.gz

    Výstup:
        - png výsledkem
'''

import sys
import os.path
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt

# root of lib repository
PROJECT_ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../..')
DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')
sys.path.append(PROJECT_ROOT)

class DataShower:

    def __init__(
        self,
        infile,
        outfile
    ):
        self.infile = infile
        self.outfile = outfile


    def run(self):
        # načti
        dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
        df = pd.read_csv(self.infile.name, sep='\t', header=0, compression='gzip', index_col=0,  parse_dates="datetime", date_parser=dateparse)
        fig, axes = plt.subplots(nrows=3, ncols=1)
        for i, c in enumerate(['f1_W', 'f2_W', 'f3_W']):
            df[c].plot(ax=axes[i], title=c)
        plt.show()
        print('Obrázek zatím neukládám (nevím k čemu by byl)')


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

            default = os.path.join(os.path.expanduser(DATA_ROOT), 'energomonitor/2roky.tsv.gz')
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

            default =  os.path.join(os.path.expanduser(DATA_ROOT), 'energomonitor/graps.png')
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
            DataShower(
                infile=self.cmdLineParams.infile,
                outfile=self.cmdLineParams.outfile
            ).run()


    Program()


