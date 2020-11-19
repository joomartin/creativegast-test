from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from core.Options import Options
from shared.BaseTestCase import BaseTestCase


class Menus(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)
        self.stockseed.createWarehouse('MenuWh')
        self.stockseed.createRawMaterialWithOpening('Menükaja', '1000', '10', 'MenuWh', 'db')
        self.productseed.createCounter('Kaja',0)
        self.productseed.createProduct('Menü Leves', 'Ételek', 11111, 'Kaja', 'Menükaja')
        self.productseed.createProduct('Menü főétel', 'Ételek', 22222, 'Kaja', 'Menükaja')
        self.menu.openProducts()
        self.html.clickElement('Menü', 'a')

    @classmethod
    def tearDownClass(self):
        self.productseed.deleteProduct('Menü Leves')
        self.productseed.deleteProduct('Menü főétel')
        self.productseed.deleteCounter('Kaja')
        self.stockseed.deleteRawMaterial('Menükaja')
        self.stockseed.deleteWarehouse('MenuWh')
        super().tearDownClass()


    def testCreate(self):
        testName = 'Test menu'
        self.productseed.createMenu(testName, 'Menü Leves', 'Menü főétel')
        self.productAssert.assertMenuExists(testName, '127.00')
        self.productseed.deleteMenu(testName)

    def testUpdateMenu(self):
        testName = 'Test menu'
        modName = 'Modified menu'
        modPrice= 300
        self.productseed.createMenu(testName, 'Menü Leves', 'Menü főétel')

        self.html.clickTableElement('menu', 'id', testName, 'span', 'Szerkeszt', 'Menü')
        self.html.switchFrame('iframe')

        self.html.fillInput('Termék neve',modName)
        self.html.getElement('27%', 'td', Options(following='td//input')).clear()
        self.html.getElement('27%', 'td', Options(following='td//input')).send_keys(modPrice)
        self.html.clickElement('Rögzít')
        self.html.wait(2)

        try:
            self.html.getElement('iframe hasTwoRow', 'body', Options(htmlAttribute='class'))
        except NoSuchElementException:
            self.html.switchFrame()
        else:
            self.html.clickElement('Rögzít')
            self.html.switchFrame()

        self.html.refresh()
        self.html.search(modName, 'Menü')
        self.html.wait(3)
        self.productAssert.assertMenuExists(modName, '381.00')

        self.productseed.deleteMenu(modName)