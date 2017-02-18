#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Příklad jednduchého programu s nápovědou a logováním chyb.
"""
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

simpleProcessorDescription='''
    Toto je příklad jednoduchého programu s nápovědou v příkazové řádce.
'''

import sys
import os

# root of lib repository
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

from cmdLine.processor import Processor
from cmdLine.cmdLineParser import CmdLineParser


class SampleProcessor(Processor, CmdLineParser):
    '''
    Viz text v napovede.
    '''

    def __init__(self, isChildCommandLineParser = False):
        # zpracuje příkazovou řádku
        CmdLineParser.__init__(
            self,
            description=simpleProcessorDescription,
            # použije se v případě sub-parseru jako popis
            subCommandHelp='minimální příklad processoru s příkazovou řádkou',
            isChildCommandLineParser=isChildCommandLineParser)
        # spustí program, zachytí výjimky
        if not self.isChildCommandLineParser:  # podmínka je zde jen v případě, že chceme použít objekt, jako pod-příkaz
            Processor.__init__(self)

    def run(self):
        print('Provádím metodu run.')
        print('Zkus volat program s parametrem -h.')


if __name__ == '__main__':
    # vytvoří objekt programu a spustí ho
    SampleProcessor()
