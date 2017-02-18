#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

description = '''
    Příklad jednduchého programu s příkazy, které mají své vlastní parametry.

    Ukazuje, jak připojit hotové procesory (simpleProcessor.py a simpleIoProcessor)
    jako pod-procesory volané příkazy (p1 nebo p2)
'''

import sys
import os

# root of lib repository
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
from cmdLine.processor import Processor
from cmdLine.cmdLineParser import ParentCmdLineParser
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import simpleProcessor
import simpleIoProcessor



class SampleParentProcessor(Processor, ParentCmdLineParser):
    '''
    Viz parametr description.
    '''

    def __init__(self):
        # zpracuje příkazovou řádku
        ParentCmdLineParser.__init__(
            self,
            description=description,
            subParserParams={
                'help': 'Každý <příkaz> má pak své vlastní argumenty. Pro podrobnější nápovědu zadejte: <příkaz> -h',
                'dest': 'subCommand',
                'title': 'Seznam akceptovaných příkazů:',
                'metavar': '<příkaz>'

            },
            cmdLineSubProcessors={
                'p1': simpleProcessor.SampleProcessor(isChildCommandLineParser=True),
                'p2': simpleIoProcessor.SampleProcessor(isChildCommandLineParser=True)
            }
        )
        # spustí program, zachytí výjimky
        Processor.__init__(self)


    def _addArgsToCmdLineParser(self, parserForYourParams):
        dafaultCommonArgument = '***spolecnaHodnota***'
        parserForYourParams.add_argument(
            '-c', '--common-argument',
            dest='commonArgument',
            metavar='<commonArgument>',
            help='a common argument (default:"{}")'.format(dafaultCommonArgument),
            default=dafaultCommonArgument
        )

    def run(self):
        '''
        Tady se definuje chování programu.
        '''
        print('Společný paramatr pro všechny příkazy <commonArgument>:{}'.format( self.cmdLineParams.commonArgument))
        print('Výstup z podprogramu:')
        print('======================================================================================================')
        if self.cmdLineParams.subCommand in self.cmdLineSubProcessors:
            self.cmdLineSubProcessors[self.cmdLineParams.subCommand].run()
        else:
            print('Nebyl zadán žádný příkaz.')


if __name__ == '__main__':
    # vytvoří objekt programu a spustí ho
    SampleParentProcessor()
