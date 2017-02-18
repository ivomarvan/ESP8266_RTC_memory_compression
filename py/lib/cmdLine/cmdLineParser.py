#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Abstraktní předek pro objek s vlastním command line parserem.
    Použije ho objekt, který chce dafinovat vlastnosti příkazové řádky (nápověda, parametry, jejich typ).
    Může se použít:
    a) samostatně v jedné úrovní
    b) kaskádovitě, kdy se definují variaty v závislosti na určitém parametru.
       Typicky má program více příkazů a ty mají různé parametry.

    Příklady jsou v adresáři samples.
"""
__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

import argparse

class CmdLineParserBase:
    '''
    Abstraktní interface s požností definovat položky parseru
    '''
    def _addArgsToCmdLineParser(self, parserForYourParams):
        '''
        Sem patří definice vlastnotí příkazové řádky.
        Celé nebo části v případě použití subparseru.
        '''
        pass


class CmdLineParser(CmdLineParserBase):
    '''
    Obvyklý jednoduchý parser příkazové řádky
    '''
    def __init__(
            self,
            description=None,
            prog=None,
            usage=None,
            epilog=None,
            parents=[],
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prefix_chars='-',
            fromfile_prefix_chars=None,
            argument_default=None,
            conflict_handler='error',
            add_help=True,
            isChildCommandLineParser = False,
            subCommandHelp=None  # použije se v případě sub-parseru jako popis
    ):
        self.cmdLineParams = argparse.Namespace()
        self.cmdLineParser = argparse.ArgumentParser(
            prog=prog,
            usage=usage,
            description=description,
            epilog=epilog,
            parents=parents,
            formatter_class=formatter_class,
            prefix_chars=prefix_chars,
            fromfile_prefix_chars=fromfile_prefix_chars,
            argument_default=argument_default,
            conflict_handler=conflict_handler,
            add_help=add_help
        )
        self.crationParams = {
            'prog':prog,
            'usage':usage,
            'description':description,
            'epilog':epilog,
            'parents':parents,
            'formatter_class':formatter_class,
            'prefix_chars':prefix_chars,
            'fromfile_prefix_chars':fromfile_prefix_chars,
            'argument_default':argument_default,
            'conflict_handler':conflict_handler,
            'add_help':add_help,
            'help':subCommandHelp
        }

        self.isChildCommandLineParser = isChildCommandLineParser
        if not isChildCommandLineParser:
            self._addArgsToCmdLineParser(self.cmdLineParser)
            self.cmdLineParser.parse_args(namespace=self.cmdLineParams)


class ParentCmdLineParser():
    def __init__(
        self,
        description=None,
        prog=None,
        usage=None,
        epilog=None,
        parents=[],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prefix_chars='-',
        fromfile_prefix_chars=None,
        argument_default=None,
        conflict_handler='error',
        add_help=True,
        subParserParams={},
        cmdLineSubProcessors={}, # {commandOption1: commandParser1, ....}
    ):
        self.cmdLineParams = argparse.Namespace()
        self.cmdLineParser = argparse.ArgumentParser(
            prog=prog,
            usage=usage,
            description=description,
            epilog=epilog,
            parents=parents,
            formatter_class=formatter_class,
            prefix_chars=prefix_chars,
            fromfile_prefix_chars=fromfile_prefix_chars,
            argument_default=argument_default,
            conflict_handler=conflict_handler,
            add_help=add_help
        )
        self._addArgsToCmdLineParser(self.cmdLineParser)

        self.cmdLineSubProcessors = cmdLineSubProcessors
        self.subParsers = self.cmdLineParser.add_subparsers(**subParserParams)

        for name in cmdLineSubProcessors:
            processorWithParser = cmdLineSubProcessors[name]
            subParserParams = processorWithParser.crationParams
            childParser = self.subParsers.add_parser(name, **subParserParams)
            processorWithParser.cmdLineParser = childParser
            processorWithParser.cmdLineParams = self.cmdLineParams
            processorWithParser._addArgsToCmdLineParser(childParser)

        self.cmdLineParser.parse_args(namespace=self.cmdLineParams)
