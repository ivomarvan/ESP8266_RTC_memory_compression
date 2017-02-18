# -*- coding: utf-8 -*-
"""
    Čte setříděný *.tsv (*.tsv.gz) soubor.
    Pokud to lze, tak pro dané id vrací řádku ze souboru.
    Jinak vrací None
"""

__author__ = "Ivo Marvan"
__email__ = "ivo@wikidi.com"

from tsvFileReader import TsvFileReader

class OrderError(Exception):
    """Base class for exceptions in this module."""
    pass

class SortedFileReader(TsvFileReader):
    """
    Čte postupně z textového souboru setříděného podle jednoho sloupečku.
    Detaily viz  getRowForId(..)
    """


    def __init__(self, fullFileName, columnWithId=0):
        super().__init__(fullFileName)
        self.columnWithId = columnWithId
        self.lastId = None # ještě se nic nehledalo
        self.currentId = None
        self.countOfRows = 0
        self.currentRow = None
        self.firstReading = True



    def getRowForId(self, id, skipRowsWithSameId=True):
        """
        Pro zadané id dá buď řádek ze souboru, ve kterém je toto id v daném sloupečku,
        nebo vrátí None, když tam není,
        nebo vyhodí vyjímku, když je soubor špatně setříděn.
        """
        if id is None or id is False:
            return None
        if self.firstReading:
            # první čtení
            self._readNext()
            self.firstReading = False
        while self.currentRow is not None and self.currentId < id:
            # není konec a požadované ID je větší, než aktuální ID v souboru
            self._readNext()
        if self.currentId == id:
            # našel se řádek se shodou
            currentRow = self.currentRow
            self._readNext()
            while skipRowsWithSameId and self.currentId == id and self.currentRow is not None:
                self._readNext()
            return currentRow
        else:
            # řádek s ID == $rowId se nenašel
            return None


    def getCountOfRows(self):
        return self.countOfRows

    def _readNext(self):
        """
        Přečte další řádek. Počítá neprázdné řádky.
        Pamatuje si aktuální a poslední ID
        Při špatně setříděném souboru vyhodí vyjimku.
        """
        self.currentRow = self.getRow(True)
        if self.currentRow is not None:
            self.countOfRows += 1
            if len(self.currentRow) > self.columnWithId:
                self.lastId = self.currentId
                self.currentId = self.currentRow[self.columnWithId]
                if self.currentId is not None and self.lastId is not None and self.currentId < self.lastId:
                    raise OrderError(
                        'In file {} on row {} bad order ({} ×{})'.format(
                            self.file.name, self.getCountOfRows(), self.currentId, self.lastId)
                    )

        return self.currentRow





