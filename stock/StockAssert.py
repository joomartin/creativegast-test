import unittest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy


class StockAssert(unittest.TestCase):

    def __init__(self, htmlProxy, driver):
        super().__init__()
        self.html = htmlProxy
        self.menu = MainMenuProxy(driver)

    def assertWarehouseExist(self, name, tab):
        self.assertTrue(self.html.getElementInTable(name, 'storages', tab).is_displayed())

    def assertWarehouseNotExist(self, name, tab):
        with self.assertRaises(NoSuchElementException):
            self.html.getElementInTable(name, 'storages', tab)

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

    def assertStock(self, materialName, whName, qty):
        tab = 'Raktárkészlet'
        self.menu.openStocks()

        self.html.clickTableDropdown(materialName, 'Raktárak', tab)
        self.html.switchFrame('iframe')
        if qty != '0':
            stock = self.html.getElement(whName, 'td', Options(following='td//following::td')).text
            self.assertEqual(stock,qty)
        else:
            with self.assertRaises(NoSuchElementException):
                self.html.getElement(whName, 'td')

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))

        self.html.clickTableDropdown(materialName, 'Készlet', tab)
        self.html.switchFrame('iframe')
        if qty != '0':
            stock = self.html.getElement(whName, 'td', Options(following='td//following::td')).text
            self.assertEqual(stock, qty)
        else :
            with self.assertRaises(NoSuchElementException):
                self.html.getElement(whName, 'td')

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))

        self.html.clickElement('Raktárak', 'a')

        self.html.clickElement(None,
                               "//tr[contains(., '"+ whName +"')]//a[contains(@class, 'stock') and contains(@class, 'actionButton')]",
                               Options(uniqueSelector=True))

        self.html.switchFrame("iframe")

        if qty != '0':
            stock = self.html.getElement(materialName, 'td', Options(following='td')).text
            self.assertEqual(stock, qty)
        else:
            with self.assertRaises(NoSuchElementException):
                self.html.getElement(materialName, 'td')

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        self.menu.openStocks()



    def assertDeletedMaterial(self, materialName, whName):
        self.html.clickElement('Raktárak', 'a')

        self.html.clickElement(None,
                               "//tr[contains(., '" + whName + "')]//a[contains(@class, 'stock') and contains(@class, 'actionButton')]",
                               Options(uniqueSelector=True))

        self.html.switchFrame("iframe")

        with self.assertRaises(NoSuchElementException):
            self.html.getElement(materialName, 'td')

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        self.menu.openStocks()

