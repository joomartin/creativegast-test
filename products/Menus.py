from selenium.common.exceptions import NoSuchElementException
from shared.TestData import TestData as data

from core.Options import Options
from shared.BaseTestCase import BaseTestCase


class Menus(BaseTestCase):
    modifiedName = 'Heti menu'
    modifiedPrice = '300'
    modifiedGrossPrice = None

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)
        self.modifiedGrossPrice = self.html.extendedRound(int(self.modifiedPrice) * 1.27, 2)
        
    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def setUp(self):
        def wrapper():
            self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'], module=True)
            self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Bundas_kenyer']['Name'],
                                                        data.RawMaterial['Bundas_kenyer']['GrossPrice'],
                                                        data.RawMaterial['Bundas_kenyer']['Quantity'],
                                                        data.WareHouses['Szeszraktár']['Name'],
                                                        data.RawMaterial['Bundas_kenyer']['ME'], module=True)
            self.productseed.createCounter(data.Counter['TestCounter']['Name'], data.Counter['TestCounter']['Position'],
                                           module=True)
            self.productseed.createProduct(data.Product['Babgulyás']['Name'], data.ProductGroup['Egyeb']['Name'],
                                           data.Product['Babgulyás']['Code'], data.Counter['TestCounter']['Name'],
                                           data.RawMaterial['Bundas_kenyer']['Name'], module=True)
            self.productseed.createProduct(data.Product['Palacsinta']['Name'], data.ProductGroup['Egyeb']['Name'],
                                           data.Product['Palacsinta']['Code'], data.Counter['TestCounter']['Name'],
                                           data.RawMaterial['Bundas_kenyer']['Name'], module=True)
            self.html.refresh()
            self.html.clickElement('Menü', 'a')

        super(Menus, self).runTest(wrapper, 'menus-setUp')

    def tearDown(self):
        try:
            self.productseed.deleteMenu(data.Menu['NapiMenu']['Name'])
        except Exception:
            pass
        try:
            self.productseed.deleteMenu(self.modifiedName)
        except Exception:
            pass
        try:
            self.productseed.deleteProduct(data.Product['Babgulyás']['Name'], module=True)
        except Exception:
            pass
        try:
            self.productseed.deleteProduct(data.Product['Palacsinta']['Name'])
        except Exception:
            pass
        try:
            self.productseed.deleteCounter(data.Counter['TestCounter']['Name'], module=True)
        except Exception:
            pass
        try:
            self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        except Exception:
            pass
        try:
            self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)
        except Exception:
            pass

    def testCreate(self):
        def wrapper():
            self.productseed.createMenu(data.Menu['NapiMenu']['Name'], data.Product['Babgulyás']['Name'], data.Product['Palacsinta']['Name'], data.Menu['NapiMenu']['Price'])
            self.productAssert.assertMenuExists(data.Menu['NapiMenu']['Name'], data.Menu['NapiMenu']['GrossPrice'])

        super(Menus, self).runTest(wrapper, 'menus-testCreate')

    def testUpdateMenu(self):
        def wrapper():
            self.productseed.createMenu(data.Menu['NapiMenu']['Name'], data.Product['Babgulyás']['Name'], data.Product['Palacsinta']['Name'], data.Menu['NapiMenu']['Price'])

            self.html.clickTableElement('menu', 'id', data.Menu['NapiMenu']['Name'], 'span', 'Szerkeszt', 'Menü')
            self.html.switchFrame('iframe')

            self.html.fillInput('Termék neve', self.modifiedName)
            self.html.getElement('27%', 'td', Options(following='td//input')).clear()
            self.html.getElement('27%', 'td', Options(following='td//input')).send_keys(self.modifiedPrice)
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
            self.html.search(self.modifiedName, 'Menü')
            self.html.wait(3)
            self.productAssert.assertMenuExists(self.modifiedName, str(self.modifiedGrossPrice))

        super(Menus, self).runTest(wrapper, 'menus-testUpdateMenu')

