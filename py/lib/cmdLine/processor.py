#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Předek pro obvyklý program s parametry v příkazové řádce
"""
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

import sys
import logging
import os
# root of lib repository
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from cmdLine.cmdLineParser import CmdLineParser


class Processor():
    '''
    Viz text v napovede.
    '''

    def __init__(self, loggingLevel = logging.WARNING):
        # inicializace příkazové řádky
        logging.basicConfig(level=loggingLevel)
        self.log = logging.getLogger(os.path.abspath(__file__))
        self.main()

    def run(self):
        '''
        Výkonná část programu
        '''
        raise NotImplementedError('Do not create instance of abstract class ' + self.__class__.__name__)


    def main(self):
        try:
            self.run()
        except Exception as e:
            self.log.exception('args: {0}'.format(sys.argv))
            exit(1)

