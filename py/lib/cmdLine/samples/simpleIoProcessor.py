#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

simpleProcessorIoDescription = '''
    Příklad jednduchého programu s nápovědou, logováním chyb a parametry:
        * vstupní soubor
        * výstupní soubor
        * mod pro debugování

     Navíc je přidán nepovinný uživatelský parametr -u.
'''

import sys
import os

# root of lib repository
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
from cmdLine.processor import Processor
from cmdLine.cmdLineParser import CmdLineParser
from cmdLine.stdIoParams import StdIoParams

class SampleProcessor(Processor, CmdLineParser, StdIoParams):
    '''
    Viz parametr description.
    '''

    def __init__(self, isChildCommandLineParser = False):
        # zpracuje příkazovou řádku
        CmdLineParser.__init__(
            self,
            description=simpleProcessorIoDescription,
            subCommandHelp='program se standardními I/O parametry', # použije se v případě sub-parseru jako popis
            isChildCommandLineParser=isChildCommandLineParser
        )
        # spustí program, zachytí výjimky
        if not self.isChildCommandLineParser:  # podmínka je zde jen v případě, že chceme použít objekt, jako pod-příkaz
            Processor.__init__(self)


    def _addArgsToCmdLineParser(self, parserForYourParams):
        # add default arguments
        StdIoParams._addArgsToCmdLineParser(self, parserForYourParams)

        dafaultUserArgument = 'ABC'
        parserForYourParams.add_argument(
            '-u', '--user-argument',
            dest='userArgument',
            metavar='<userArgument>',
            help='a user argument (default:"{}")'.format(dafaultUserArgument),
            default=dafaultUserArgument
        )

    def run(self):
        '''
        Tady se definuje chování programu.
        '''
        print(
            '''
            -------------------------------------------------------------------------------------------------
            Provádím metodu run.

            Zkus volat program s parametrem -h.

            Vyzkušej také zadat jiné parametry z příkazové řádky.
            -------------------------------------------------------------------------------------------------
            '''
        )
        if self.cmdLineParams.debugMode:
            print('\n* Toto je debug mód')

        print('Parametry z příkazové řádky:')
        dictOfParams = vars(self.cmdLineParams)
        for i in dictOfParams:
            print('{}:{}'.format(i, dictOfParams[i]))

if __name__ == '__main__':
    # vytvoří objekt programu a spustí ho
    SampleProcessor()
