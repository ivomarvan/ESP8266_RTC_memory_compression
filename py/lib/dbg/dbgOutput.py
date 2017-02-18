#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__description__ = '''\
   Vypisuje dbg hlášky do std err.
'''

__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

import sys

class DbgOutput:
    
    def __init__(self, isActive=False, outStream=sys.stderr):
        self.isActive = isActive
        self.outStream = outStream


    def __deepcopy__(self, memoDictForRecursion):
        return DbgOutput(self.isActive, self.outStream)


    def write(self, *args):
        '''
        Vypisuje argumenty bez nového řádku na konci.
        Vhodné pro skládání více věcí na jednom řádku.
        Například info o spuštěném procesu a pak po jeho ukončení na stejý řáde info o tom, jak to dopadlo.
        '''
        if self.isActive:
            for i, msg in enumerate(args):
                if i:
                    self.outStream.write(' ')
                self.outStream.write(str(msg))
            self.outStream.flush()

    def print(self, *args):
        '''
        Vypisuje argumenty včetně nového řádku na konci.
        '''
        if self.isActive:
            for i, msg in enumerate(args):
                if i:
                    self.outStream.write(' ')
                self.outStream.write(str(msg))
            self.outStream.write('\n')
            self.outStream.flush()

    def __getstate__(self):
        self.outStream = None
        return self.__dict__

    def __setstate__(self, state):
        self.isActive = state['isActive']
        self.outStream = sys.stderr
