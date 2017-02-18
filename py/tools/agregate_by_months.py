#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"
__description__ = '''
    Vypíše statistiku po měsících.

    Inputs:
        - vstupní adresář s *.csv.gz

    Výstup:
        - tsv výstup z výsledkem
'''

import sys
import os.path
import pandas as pd
from collections import OrderedDict
import math
from pprint import pprint


# root of lib repository
PROJECT_ROOT = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../..')
DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')
sys.path.append(PROJECT_ROOT)

import py.lib.std as std




class DataProcessor:

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
        data = pd.read_csv(self.infile.name, sep='\t', header=0, compression='gzip', index_col=0,  parse_dates="datetime", date_parser=dateparse)

        agregationTime  = {
            'mounth': list(range(1,13)),
            'hour': list(range(0, 24))
        }


        self.outfile.write('{}  -  {}\n'.format(data.index[0], data.index[-1]))

        for aggrName, aggrTimes in agregationTime.items():
            self.outfile.write('\n\nagregation by\t' + aggrName + '\n')
            for aggrFunct in ['mean', 'min', 'max']:
                self.outfile.write('\n\nfunct\t' + aggrFunct + '\n')
    
                #header
                for i, col in enumerate([aggrName] + list(data.columns)):
                    if i:
                        self.outfile.write('\t')
                    self.outfile.write(col)
                self.outfile.write('\n')
    
                # agregace po měsící, nabastlený TSV výstup
                for timeItem  in aggrTimes:
                    self.outfile.write(str(timeItem))
                    for columnName in data.columns:
                        columnData = data[columnName]
    
                        self.outfile.write('\t')
                        if aggrName == 'mounth':
                            aggr = columnData[columnData.index.month == timeItem]
                        elif aggrName == 'hour':
                            aggr = columnData[columnData.index.hour == timeItem]
                        else:
                            raise Exception('Uknown aggrName:'+aggrName)
                        if aggrFunct=='mean':
                            value = aggr.mean()
                        elif aggrFunct=='min':
                            value = aggr.min()
                        elif aggrFunct=='max':
                            value = aggr.max()
                        self.outfile.write(str(round(value, 2)))
                    self.outfile.write('\n')



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

            default =  os.path.join(os.path.expanduser(DATA_ROOT), 'energomonitor/all.my_monts.tsv')
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
            DataProcessor(
                infile=self.cmdLineParams.infile,
                outfile=self.cmdLineParams.outfile
            ).run()


    Program()


