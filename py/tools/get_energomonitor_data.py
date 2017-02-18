#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"
__description__ = '''
    Dá data rostroušená v v mnoha csv souborech v různých formátech, do jednoho souboru.
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


    COLUMNS_DEF = OrderedDict()
    COLUMNS_DEF["datetime"] = ["Unnamed: 0"]
    COLUMNS_DEF["f1_czk"] = ["Hlavní odběr, Fáze 1 [CZK] #1", "Hlavní odběr, Fáze 1 [CZK] #2", "Sensor 0, ph1 [CZK] #1"]

    COLUMNS_DEF["f2_czk"]   = ["Hlavní odběr, Fáze 2 [CZK] #2", "Hlavní odběr, Fáze 2 [CZK] #3", "Sensor 0, ph2 [CZK] #2"]
    COLUMNS_DEF["f3_czk"]   = ["Hlavní odběr, Fáze 3 [CZK] #3", "Hlavní odběr, Fáze 3 [CZK] #4", "Sensor 0, ph3 [CZK] #3"]
    COLUMNS_DEF["f1_Wh"]    = ["Hlavní odběr, Fáze 1 [Wh] #5", "Hlavní odběr, Fáze 1 [Wh] #6", "Sensor 0, ph1 [Wh] #5"]
    COLUMNS_DEF["f2_Wh"]    = ["Hlavní odběr, Fáze 2 [Wh] #6", "Hlavní odběr, Fáze 2 [Wh] #7", "Sensor 0, ph2 [Wh] #6"]
    COLUMNS_DEF["f3_Wh"]    = ["Hlavní odběr, Fáze 3 [Wh] #7", "Hlavní odběr, Fáze 3 [Wh] #8", "Sensor 0, ph3 [Wh] #7"]
    COLUMNS_DEF["f1_W"]     = ["Hlavní odběr, Fáze 1 [W] #9", "Hlavní odběr, Fáze 1 [W] #10", "Sensor 0, ph1 [W] #9"]
    COLUMNS_DEF["f2_W"]     = ["Hlavní odběr, Fáze 2 [W] #10", "Hlavní odběr, Fáze 2 [W] #11", "Sensor 0, ph2 [W] #10"]
    COLUMNS_DEF["f3_W"]     = ["Hlavní odběr, Fáze 3 [W] #11", "Hlavní odběr, Fáze 3 [W] #12", "Sensor 0, ph3 [W] #11"]

    OUT_COLUMNS_NAMES = list(COLUMNS_DEF.keys())


    def __init__(
        self,
        inDir,
        outfile
    ):
        self.inDir = inDir
        self.outfile = outfile

        self.maxCountOfFiles = -1

        self.columnsDict = self.createColumnsDictionary()
        self.wholeDataFrame = pd.DataFrame(columns=self.OUT_COLUMNS_NAMES)



    def createColumnsDictionary(self):
        retDict = {}
        for newColumnName,columnNamesVariants in self.COLUMNS_DEF.items():
            for columnNameVariant in columnNamesVariants:
                if columnNameVariant in retDict:
                    raise Exception("Duplicitní jméno souboru:" + columnNameVariant)
                else:
                    retDict[columnNameVariant] = newColumnName;
        return retDict

    def run(self):
        # posbírej
        self.genWholeDataFrame()

        # sort
        self.wholeDataFrame = self.wholeDataFrame.sort(['datetime'])

        # ulož
        self.wholeDataFrame.to_csv(self.outfile, index=False, sep='\t')

    def genWholeDataFrame(self):

        for root, dirs, files in sorted(os.walk(self.inDir)):
            i = 0
            for file in sorted(files):
                if file.endswith('csv.gz'):
                    inFileName = os.path.join(root, file)
                    self.processFile(inFileName)
                if i >= self.maxCountOfFiles > 0:
                    break
                i += 1

    def processFile(self, inFileName):
        oneFileData = pd.read_csv(inFileName, sep=',', header=0, compression='gzip')

        newColumns = []
        columnsToRemove =  []
        for column in oneFileData:
            if column in self.columnsDict:
                newColumns.append(self.columnsDict[column])
            else:
                columnsToRemove.append(column);

        for columnToRemove in columnsToRemove:
            del oneFileData[columnToRemove]

        oneFileData.columns = newColumns

        self.wholeDataFrame = self.wholeDataFrame.append(oneFileData)




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

            default = os.path.join(os.path.expanduser(DATA_ROOT), 'energomonitor')
            parser.add_argument(
                '-id', '--input-dir',
                dest='inDir',
                metavar='<inDir>',
                type=std.readableDir,
                required=False,
                help='Adresář predict odkud se čtou vstupní soubory obrázků. (default: ' + str(default) + ')',
                default=default
            )

            default =  os.path.join(os.path.expanduser(DATA_ROOT), 'energomonitor/all.tsv')
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
            DataProcessor(
                inDir=self.cmdLineParams.inDir,
                outfile=self.cmdLineParams.outfile
            ).run()


    Program()


    '''
    Jak s daty pak pracovat (např v Ipython)
    d =  pd.read_csv('all.tsv.gz', sep='\t', header=0, compression='gzip', index_col=0,  parse_dates="datetime", date_parser=dateparse)
    '''