import unittest

from selenium.common.exceptions import NoSuchElementException
from core.Options import Options


class StockAssert(unittest.TestCase):

    def __init__(self, htmlProxy):
        super().__init__()
        self.html = htmlProxy

    def assertWarehouseExist(self, name, tab):
        self.assertTrue(self.html.getElementInTable(name, 'sorting_1', tab).is_displayed())

    def assertWarehouseNotExist(self, name, tab):
        with self.assertRaises(NoSuchElementException):
            self.html.getElementInTable(name, 'sorting_1', tab)

    def assertDialogDisplayed(self):
        self.assertTrue(self.html.getElement('iframe', 'body', Options(htmlAttribute='class')).is_displayed())

    def assertMaterialExist(self, materialName, tab):
        self.html.search(materialName, tab)
        self.assertTrue(self.html.getElement(materialName, 'td').is_displayed())
        self.html.search('', tab)
        #self.assertTrue(self.html.getElementInTable(materialName, 'td', tab).is_displayed())

    def assertAllergenExist(self, allergenName):
        self.assertTrue(self.html.getElement(allergenName, 'td').is_displayed())

    def assertStockMovementExist(self, fromWh, toWh):
        self.assertTrue(self.html.getElement(fromWh, 'td').is_displayed())
        self.assertTrue(self.html.getElement(toWh, 'td').is_displayed())








