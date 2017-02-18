# -*- coding: utf-8 -*-
"""
    Soubor *.tsv nebo *.tsv.gz.
"""

__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

import csv
import gzip
import codecs

class TsvFileReader:
    """
    Soubor, který je buď *.tsv, nebo *.tsv.gz.
    Slouží k jednomu sekvečnímu přečtení.
    """

    def __init__(self, fullFileName, delimiter='\t', quotechar='\x01', dialect='excel'):
        """
        Otevře soubor
        """
        self.gzipped = False
        if fullFileName.endswith('.gz'):
            self.file = gzip.open(fullFileName)
            self.gzipped = True
            csvfile = codecs.iterdecode(self.file, 'utf8')

        else:
            self.file = open(fullFileName, mode='r', encoding='utf8')
            csvfile = self.file

        self.csvReader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar, dialect=dialect)


    def __del__(self):
        try:
            self.file.close()
        except AttributeError:
            # hack for python >= 3.4.0
            pass

    def getRow(self, skipEmptyRows=True):
        """
        Načte a vrátí jeden řádek.
        Pokud již řádek nenajde, vrátí None.

        Pokud je skipEmptyRows==true, vrací neprázdné řádky a ostatní přeskakuje.

        @return array/None
        """
        try:
            # prázdný řádek ... row==[], konec ... vyjimka
            row = next(self.csvReader)

            while skipEmptyRows	and not row:    # přeskakování prázdných řádků je vyžadováno a je prázdný
                row = next(self.csvReader)

            return row

        except StopIteration as e:
            return None

    def getLineNumber(self):
        return self.csvReader.line_num