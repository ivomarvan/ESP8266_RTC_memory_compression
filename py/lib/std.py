# -*- coding: utf-8 -*-
"""
    @see vícenásobně použitelné funkce
"""

__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

import os.path
import argparse
import math
import sys

def readableDir(string):
    dir = str(string)

    if not os.path.isdir(dir):
        msg = "'{0}' is  not existing directory".format(dir)
        raise argparse.ArgumentTypeError(msg)
    elif not os.access(dir, os.R_OK):
        msg = "{0}' is not accessible directory".format(dir)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dir


def writableDir(string):
    dir = str(string)

    if not os.path.isdir(dir):
        # pokus se adresář vytvořit
        try:
            os.makedirs(dir, exist_ok=True)
            sys.stderr.write('Directory "{0}" created.\n'.format(dir))
        except OSError as e:
            msg = "Cennot create '{0}' directory.\n{1}".format(dir, e.strerror)
            raise argparse.ArgumentTypeError(msg)
    if not os.access(dir, os.W_OK):
        msg = "'{0}' is not accessible directory for writning".format(dir)
        raise argparse.ArgumentTypeError(msg)
    return dir

def isNumber(s):
    '''
    Zjistí, zda se řetězec/číslo dá považovat za číslo float.
    Nekonečno se za číslo nepovažuje
    '''
    try:
        n = float(s)
        if math.isinf(n) or math.isnan(n):
            return False
        return True
    except TypeError:
        return False
    except ValueError:
        return False