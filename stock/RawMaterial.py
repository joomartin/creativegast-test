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
from shared.DataSeed import DataSeed


class RawMaterial(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openStocks()
        self.data = DataSeed(self.driver)

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def createRawMaterial(self, materialName, ME):
        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyersanyag neve', materialName)
        self.html.clickDropdown('ME', ME)
        self.html.clickDropdown('Raktár', 'Pult')
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()
        self.stockAssert.assertMaterialExist(materialName, 'Raktárkészlet')

    def deleteRawMaterial(self, name):
        self.html.refresh()

        self.html.wait(2)
        self.html.search(name, 'Raktárkészlet')
        self.html.wait(2)
        #currWindow = self.html.getTab('Raktárkészlet')
        #self.html.clickElement(name, 'td', Options(following='a'), element = currWindow)
        self.html.clickTableDropdown(name, 'Törlés', 'Raktárkészlet')
        self.html.clickElement('Igen')
        self.html.wait(2)
        self.html.search('', 'Raktárkészlet')
        self.html.wait(2)

    def testCreate(self):
        testName = 'Abszint'
        self.data.createRawMaterial(testName, 'liter', 'Pult')
        self.data.deleteRawMaterial(testName)


    def testUpdate(self):
        testName = 'Abszint'
        ME = 'liter'
        price = '1 010.00'

        self.data.createRawMaterial(testName, 'liter', 'Pult')
        #self.html.search(testName, 'Raktárkészlet')
        #self.html.clickElement(testName, 'td', Options(following='a'))
        self.html.clickTableDropdown(testName, 'Szerkeszt', 'Raktárkészlet')
        self.html.switchFrame('iframe')

        self.html.fillInput('Bruttó beszerzési egységár', price)
        self.html.clickElement('Rögzít')
        self.html.switchFrame()
        self.html.refresh()

        self.html.search(testName, 'Raktárkészlet')
        new = self.html.getTxtFromTable('1', '6', 'components')
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

        self.html.search(testName, 'Raktárkészlet')
        quantity = self.html.getTxtFromTable(1, 3, 'components')
        self.assertEqual('10.00', quantity)

        netPrice = self.html.getTxtFromTable(1, 5, 'components')
        self.assertEqual(netPrice, '787.40')

        nettValue = self.html.getTxtFromTable(1, 7, 'components')
        self.assertEqual(nettValue, '7 874.02')

        self.html.clickTableDropdown(testName, 'Raktárak', 'Raktárkészlet')
        self.html.switchFrame('iframe')

        whause = self.html.getTxtFromTable(2, 2)
        self.assertEqual(whause, 'Pult')

        grossPrice = self.html.getTxtFromTable(2, 3)
        self.assertEqual(grossPrice, '1000')

        qty = self.html.getTxtFromTable(2, 4)
        self.assertEqual(qty, '10')

        whValue = self.html.getTxtFromTable(2, 5)
        self.assertEqual(whValue, '10000')

        # self.html.pressKey('iframe', 'body', Keys.ESCAPE, Options(htmlAttribute='class'))
        # self.html.switchFrame()
        # self.menu.openStocks()
        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))

        self.stockAssert.assertStock(testName, 'Pult', '10')

        self.deleteRawMaterial(testName)

        self.stockAssert.assertDeletedMaterial(testName, 'Pult',)

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
        self.html.search(testName, 'Raktárkészlet')
        self.stockAssert.assertMaterialExist(testName, 'Raktárkészlet')

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
        ME = 'liter'

        self.data.createRawMaterial(testName, 'liter', 'Pult')
        # self.html.search(testName, 'Raktárkészlet')
        # self.html.clickElement(testName, 'td',  Options(following='a'))
        self.html.clickTableDropdown(testName, 'Szerkeszt', 'Raktárkészlet')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyitó mennyiség', '10')
        self.html.clickDropdown('Raktár', 'Pult')
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

        self.html.clickTableDropdown(testName, 'Selejt', 'Raktárkészlet')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Raktár', 'Pult')
        self.html.fillInput('Mennyiség', '5')
        self.html.clickElement('Üveg összetört')
        self.html.switchFrame()
        self.html.refresh()

        self.html.search(testName, 'Raktárkészlet')
        qty = self.html.getTxtFromTable(1, 3, 'components')
        self.assertEqual(qty, '5.00')

        self.stockAssert.assertStock(testName, 'Pult', '5')

        self.data.deleteRawMaterial(testName)

        self.stockAssert.assertDeletedMaterial(testName, 'Pult',)

    def testOpeningButton(self):
        testName = 'Abszint'
        ME = 'liter'
        qty = '100'

        self.createRawMaterial(testName, ME)

        self.html.clickElement(testName, 'td', Options(following='a'))
        self.html.clickElement('Nyitókészlet', 'a')

        self.html.switchFrame('iframe')
        input = self.html.getElement(testName, 'td', Options(following='input'))
        input.send_keys(qty)

        self.html.clickDropdown(testName, 'Dugipia raktár', 'td')
        self.html.clickElement('Rögzít', 'span', waitSeconds=2)

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))


        self.html.refresh()
        self.stockAssert.assertStock(testName, 'Dugipia raktár', qty)








