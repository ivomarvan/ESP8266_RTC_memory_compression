# -*- coding: utf-8 -*-
"""
    Gzipovaný soubor pro zápis
"""

__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

import csv
import gzip
import codecs
import sys

class TsvGzipWriter:
    """
    Soubor, ktery je *.tsv.gz a lze do nej zapisovat.
    Zvlastni trida je to pro osetreni zapisu UTF-8 do gzipovaneho souboru.
    """

    def __init__(self, fullFileName, delimiter='\t', quotechar='\x01', quoting=csv.QUOTE_NONE, lineterminator="\n"):
        """
        Otevře soubor
        """
        if fullFileName.endswith('.gz'):
            self.file = gzip.GzipFile(fullFileName, 'wb')
            UTF8Writer = codecs.getwriter('utf8')
            self.csvWriter = csv.writer(
                UTF8Writer(self.file),
                delimiter=delimiter, quotechar=quotechar, quoting=quoting, lineterminator=lineterminator
            )
        else:
            if fullFileName == '<stdout>':
                self.file = sys.stdout
            else:
                self.file = open(fullFileName, 'w', encoding='utf8', newline='')
            self.csvWriter = csv.writer(
                self.file, delimiter=delimiter, quotechar=quotechar, quoting=quoting, lineterminator=lineterminator
            )


    def writerow(self, row):
        """
        Uloží pole jako tsv řádek.
        """
        self.csvWriter.writerow(row)

    def close(self):
        self.file.close()
