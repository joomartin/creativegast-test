import unittest

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from core.HtmlProxy import HtmlProxy
from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy
from stock.StockAssert import StockAssert
from shared.BaseTestCase import BaseTestCase
from stock.RawMaterial import RawMaterial


class Allergens(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openStocks()
        self.html.clickElement('Allergén anyagok', 'a')

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def createAllergen(self, name, no):
        self.html.clickElement('Új allergén felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Név', name)
        self.html.fillInput('Sorszám', no)
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()
        self.stockAssert.assertAllergenExist(name)

    def deleteAllergen(self, name):
        self.html.clickElement(name, 'td[@class="sorting_1"]', Options(following='a'))
        self.html.clickElement('Igen')

    def testCreate(self):
        testName = 'Allergén teszt'
        no = 20
        self.createAllergen(testName, no)
        self.deleteAllergen(testName)

    def testUpdateAllergen(self):
        testName = 'Allergén teszt'
        no = 20
        self.createAllergen(testName, no)
        self.html.clickElement(None,
                               "//tr[contains(., '" + testName + "')]//a[contains(@class, 'edit') and contains(@class, 'actionButton')]",
                               Options(uniqueSelector=True))
        self.html.switchFrame('iframe')
        self.html.fillInput('Név', 'Allergén teszt update')
        self.html.clickElement('Rögzít')
        self.html.switchFrame()
        self.html.refresh()

        self.stockAssert.assertAllergenExist('Allergén teszt update')

        self.deleteAllergen('Allergén teszt update')

    def testAddAllergenToRawMaterial(self):
        testName = 'Allergén teszt'
        no = 20
        self.createAllergen(testName,no)
        self.html.wait()
        self.html.clickElement('Raktárkészlet', 'a')
        RawMaterial.createRawMaterial('Abszint')

        self.html.clickElement('Abszint', 'td', Options(following='a'))
        self.html.getElement('edit', 'a', Options(htmlAttribute='class')).click()
        self.html.switchFrame('iframe')

        self.html.clickElement('Allergén anyagok', 'a')
        self.html.clickElement(testName)

        self.stockAssert.assertAllergenExist(testName)

        self.html.clickElement('Rögzít')
        self.html.switchFrame()

        self.html.clickElement('Abszint', 'td', Options(following='a'))
        self.html.getElement('edit', 'a', Options(htmlAttribute='class')).click()
        self.html.switchFrame('iframe')

        self.html.clickElement('Allergén anyagok', 'a')

        self.stockAssert.assertAllergenExist(testName)
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

        RawMaterial.deleteRawMaterial('Abszint')

        self.html.clickElement('Allergén anyagok', 'a')
        self.deleteAllergen(testName)




