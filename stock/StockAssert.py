import unittest

from selenium.common.exceptions import NoSuchElementException
from core.Options import Options


class StockAssert(unittest.TestCase):

    def __init__(self, htmlProxy):
        super().__init__()
        self.html = htmlProxy

    def assertWarehouseExist(self, name):
        self.assertTrue(self.html.getElementInTable(name, 'sorting_1').is_displayed())

    def assertWarehouseNotExist(self, name):
        with self.assertRaises(NoSuchElementException):
            self.html.getElementInTable(name, 'sorting_1')

    def assertDialogDisplayed(self):
        self.assertTrue(self.html.getElement('iframe', 'body', Options(htmlAttribute='class')).is_displayed())

    def assertMaterialExist(self, materialName):
        self.assertTrue(self.html.getElement(materialName, 'td').is_displayed())










