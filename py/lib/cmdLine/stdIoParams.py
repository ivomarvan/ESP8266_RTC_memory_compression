#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Dodá do programu standardní parametry :
        * vstupní soubor
        * výstupní soubor
        * mod pro debugování

"""
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

import sys
import logging
import os
import argparse
# root of lib repository
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from cmdLine.cmdLineParser import CmdLineParserBase

class StdIoParams(CmdLineParserBase):

    def _addArgsToCmdLineParser(self, parserForYourParams):
        '''
        Sem patří definice vlastnotí příkazové řádky.
        '''
        parserForYourParams.add_argument(
            dest='infile',
            metavar='<infile>',
            nargs='?',
            type=argparse.FileType('r'),
            help='readable input file name (with full path), dafault:stdin',
            default=sys.stdin
        )

        parserForYourParams.add_argument(
            dest='outfile',
            metavar='<outfile>',
            nargs='?',
            type=argparse.FileType('w'),
            help='writable output file name (with full path), dafault:stdout',
            default=sys.stdout
        )

        parserForYourParams.add_argument(
            '-d', '--debug',
            dest='debugMode',
            help='zapisuje na výstup informace o nalezených signálech',
            default=False,
            action='store_true'
        )

