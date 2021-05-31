from selenium.common.exceptions import NoSuchElementException
from shared.TestData import TestData as data

from core.Options import Options
from shared.BaseTestCase import BaseTestCase


class Menus(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)
        
    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def setUp(self):
        self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Bundas_kenyer']['Name'],
                                                    data.RawMaterial['Bundas_kenyer']['GrossPrice'],
                                                    data.RawMaterial['Bundas_kenyer']['Quantity'],
                                                    data.WareHouses['Szeszraktár']['Name'],
                                                    data.RawMaterial['Bundas_kenyer']['ME'], module=True)
        self.productseed.createCounter(data.Counter['TestCounter']['Name'], data.Counter['TestCounter']['Position'],
                                       module=True)
        #self.productseed.createProductGroup(data.ProductGroup['Egyeb']['Name'], tab=True)
        self.productseed.createProduct(data.Product['Babgulyás']['Name'], data.ProductGroup['Egyeb']['Name'],
                                       data.Product['Babgulyás']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.productseed.createProduct(data.Product['Palacsinta']['Name'], data.ProductGroup['Egyeb']['Name'],
                                       data.Product['Palacsinta']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.html.refresh()
        self.html.clickElement('Menü', 'a')


    def tearDown(self):
        self.productseed.deleteProduct(data.Product['Babgulyás']['Name'], module=True)
        self.productseed.deleteProduct(data.Product['Palacsinta']['Name'])
        self.productseed.deleteCounter(data.Counter['TestCounter']['Name'], module=True)
        #self.productseed.deleteProductGroup(data.ProductGroup['Egyeb']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)


    def testCreate(self):
        self.productseed.createMenu(data.Menu['NapiMenu']['Name'], data.Product['Babgulyás']['Name'], data.Product['Palacsinta']['Name'], data.Menu['NapiMenu']['Price'])
        self.productAssert.assertMenuExists(data.Menu['NapiMenu']['Name'], data.Menu['NapiMenu']['GrossPrice'])
        self.productseed.deleteMenu(data.Menu['NapiMenu']['Name'])

    def testUpdateMenu(self):
        modifiedName = 'Heti menu'
        modifiedPrice= '300'
        modifiedGrossPrice = self.html.extendedRound(int(modifiedPrice) * 1.27, 2)

        self.productseed.createMenu(data.Menu['NapiMenu']['Name'], data.Product['Babgulyás']['Name'], data.Product['Palacsinta']['Name'], data.Menu['NapiMenu']['Price'])

        self.html.clickTableElement('menu', 'id', data.Menu['NapiMenu']['Name'], 'span', 'Szerkeszt', 'Menü')
        self.html.switchFrame('iframe')

        self.html.fillInput('Termék neve', modifiedName)
        self.html.getElement('27%', 'td', Options(following='td//input')).clear()
        self.html.getElement('27%', 'td', Options(following='td//input')).send_keys(modifiedPrice)
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
        self.html.search(modifiedName, 'Menü')
        self.html.wait(3)
        self.productAssert.assertMenuExists(modifiedName, str(modifiedGrossPrice))

        self.productseed.deleteMenu(modifiedName)