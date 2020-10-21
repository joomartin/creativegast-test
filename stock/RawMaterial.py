import unittest

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from core.HtmlProxy import HtmlProxy
from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy
from stock.StockAssert import StockAssert
from Config import read_section
from shared.BaseTestCase import BaseTestCase


class RawMaterial(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openStocks()

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def createRawMaterial(self, materialName):
        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyersanyag neve', materialName)
        self.html.clickDropdown('ME', 'liter')
        self.html.clickDropdown('Raktár', 'Pult')
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()
        self.stockAssert.assertMaterialExist(materialName)

    def deleteRawMaterial(self, name):
        self.html.clickElement(name, 'td', Options(following='a'))
        self.html.clickElement('Törlés', 'a', waitSeconds=2)
        self.html.clickElement('Igen')

    def testCreate(self):
        testName = 'Abszint'
        self.createRawMaterial(testName)
        self.deleteRawMaterial(testName)

    def testUpdate(self):
        testName = 'Abszint'
        price = '1 010.00'

        self.createRawMaterial(testName)
        self.html.clickElement(testName, 'td', Options(following='a'))
        self.html.getElement('edit', 'a', Options(htmlAttribute='class')).click()
        self.html.switchFrame('iframe')

        self.html.fillInput('Bruttó beszerzési egységár', price)
        self.html.clickElement('Rögzít')
        self.html.switchFrame()
        self.html.refresh()

        new = self.html.getTxtFromTable('1', '6')
        self.assertEqual(price, new)

        self.deleteRawMaterial(testName)

    def testOpening(self):
        testName = 'Abszint'

        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyersanyag neve', testName)
        self.html.fillInput('Bruttó beszerzési egységár', '1000')
        self.html.clickDropdown('ME', 'liter')
        self.html.fillInput('Nyitó mennyiség', '10')
        self.html.clickDropdown('Raktár', 'Pult')
        self.html.clickElement('Rögzít')
        self.html.switchFrame()
        self.html.refresh()

        quantity = self.html.getTxtFromTable(1, 3)
        self.assertEqual('10.00', quantity)

        netPrice = self.html.getTxtFromTable(1, 5)
        self.assertEqual(netPrice, '787.40')

        nettValue = self.html.getTxtFromTable(1, 7)
        self.assertEqual(nettValue, '7 874.02')

        self.html.clickElement(testName,'td', Options(following='a'))
        self.html.getElement('storages', 'a', Options(htmlAttribute='class')).click()
        self.html.switchFrame('iframe')

        whause = self.html.getTxtFromTable(2, 2)
        self.assertEqual(whause, 'Pult')

        grossPrice = self.html.getTxtFromTable(2, 3)
        self.assertEqual(grossPrice, '1000')

        qty = self.html.getTxtFromTable(2, 4)
        self.assertEqual(qty, '10')

        whValue = self.html.getTxtFromTable(2, 5)
        self.assertEqual(whValue, '10000')

        self.html.pressKey('iframe', 'body', Keys.ESCAPE, Options(htmlAttribute='class'))
        self.html.switchFrame()
        self.menu.openStocks()

        self.deleteRawMaterial(testName)

    def testDuplicate(self):
        testName = 'Abszint'

        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyersanyag neve', testName)
        self.html.clickDropdown('ME', 'liter')
        self.html.clickDropdown('Raktár', 'Pult')
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

        self.html.refresh()
        self.stockAssert.assertMaterialExist(testName)

        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyersanyag neve', testName)
        self.html.clickDropdown('ME', 'liter')
        self.html.clickDropdown('Raktár', 'Pult')
        self.html.clickElement('Rögzít')

        self.stockAssert.assertDialogDisplayed()

        self.html.clickElement('Mégse')
        self.html.clickElement('Igen')
        self.html.switchFrame()

        self.deleteRawMaterial(testName)

    def testWastingRawMaterial(self):
        testName = 'Abszint'

        self.createRawMaterial(testName)
        self.html.clickElement(testName, 'td',  Options(following='a'))
        self.html.getElement('edit', 'a', Options(htmlAttribute='class')).click()
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyitó mennyiség', '10')
        self.html.clickDropdown('Raktár', 'Pult')
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

        self.html.clickElement(testName, 'td',  Options(following='a'))
        self.html.getElement('waste', 'a', Options(htmlAttribute='class')).click()
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Raktár', 'Pult')
        self.html.fillInput('Mennyiség', '5')
        self.html.clickElement('Üveg összetört')
        self.html.switchFrame()
        self.html.refresh()

        qty = self.html.getTxtFromTable(1, 3)
        self.assertEqual(qty, '5.00')

        self.deleteRawMaterial(testName)

