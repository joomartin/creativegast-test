from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from shared.TestData import TestData as td

from core.Options import Options
from shared.BaseTestCase import BaseTestCase


class Menus(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)
        self.stockseed.createWarehouse(td.WareHouse['Name'], module=True)
        self.stockseed.createRawMaterialWithOpening(td.RawMaterial['Name'], td.RawMaterial['GrosPrice'], td.RawMaterial['Quantity'], td.WareHouse['Name'], td.RawMaterial['ME'], module=True)
        self.productseed.createCounter(td.Counter['Name'], td.Counter['Position'], module=True)
        self.productseed.createProductGroup(td.ProductGroup['Name'], tab=True)
        self.productseed.createProduct(td.Product['Name'], td.ProductGroup['Name'], td.Product['Code'], td.Counter['Name'], td.RawMaterial['Name'], module=True)
        self.productseed.createProduct(td.Product['Name2'], td.ProductGroup['Name'], td.Product['Code2'], td.Counter['Name'], td.RawMaterial['Name'], module=True)
        self.html.refresh()
        self.html.clickElement('Menü', 'a')

    @classmethod
    def tearDownClass(self):

        self.productseed.deleteProduct(td.Product['Name'], module=True)
        self.productseed.deleteProduct(td.Product['Name2'])
        self.productseed.deleteCounter(td.Counter['Name'], module=True)
        self.productseed.deleteProductGroup(td.ProductGroup['Name'], module=True)
        self.stockseed.deleteRawMaterial(td.RawMaterial['Name'], module=True)
        self.stockseed.deleteWarehouse(td.WareHouse['Name'], tab=True)
        super().tearDownClass()



    def testCreate(self):
        self.productseed.createMenu(td.Menu['Name'], td.Product['Name'], td.Product['Name2'], td.Menu['Price'])
        self.productAssert.assertMenuExists(td.Menu['Name'], td.Menu['GrossPrice'])
        self.productseed.deleteMenu(td.Menu['Name'])

    def testUpdateMenu(self):
        modName = 'Modified menu'
        modPrice= 300
        self.productseed.createMenu(td.Menu['Name'], td.Product['Name'], td.Product['Name2'], td.Menu['Price'])

        self.html.clickTableElement('menu', 'id', td.Menu['Name'], 'span', 'Szerkeszt', 'Menü')
        self.html.switchFrame('iframe')

        self.html.fillInput('Termék neve', td.Menu['ModifiedName'])
        self.html.getElement('27%', 'td', Options(following='td//input')).clear()
        self.html.getElement('27%', 'td', Options(following='td//input')).send_keys(td.Menu['ModifiedPrice'])
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
        self.html.search(td.Menu['ModifiedName'], 'Menü')
        self.html.wait(3)
        self.productAssert.assertMenuExists(td.Menu['ModifiedName'], '381.00')

        self.productseed.deleteMenu(td.Menu['ModifiedName'])