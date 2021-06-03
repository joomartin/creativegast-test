import unittest

from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from datetime import datetime
from shared.TestData import TestData as data


class Pizza(BaseTestCase):
    rawMaterials = ['Csirkemell', 'Finomliszt', 'Almalé', 'Hasábburgonya', 'Sonka', 'Paradicsomszósz']

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
        for material in self.rawMaterials:
            self.stockseed.createRawMaterialWithOpening(data.RawMaterial[material]['Name'],
                                                        data.RawMaterial[material]['GrosPrice'],
                                                        data.RawMaterial[material]['Quantity'],
                                                        data.RawMaterial[material]['Warehouse'],
                                                        data.RawMaterial[material]['ME'],
                                                        module=True)
        self.productseed.createCounter(data.Counter['TestCounter']['Name'], data.Counter['TestCounter']['Position'],
                                       module=True)

        self.menu.openProducts()
        self.html.clickElement('Pizza (testreszabható)', 'a')

    def tearDown(self):
        try:
            self.productseed.deleteProduct(data.Product['Sonka']['Name'], module=True)
        except Exception:
            pass
        try:
            self.productseed.deleteProduct(data.Product['Paradicsomszósz']['Name'], module=True)
        except Exception:
            pass
        try:
            self.productseed.deletePizza('Sonkás pizza', module=True)
        except Exception:
            pass
        try:
            self.productseed.deleteCounter(data.Counter['TestCounter']['Name'], module=True)
        except Exception:
            pass
        for material in self.rawMaterials:
            try:
                self.stockseed.deleteRawMaterial(data.RawMaterial[material]['Name'], module=True)
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

    @unittest.skip
    def testCreate(self):
        testName = 'Create pizza'
        self.productseed.createPizza(data.Pizza['Sonkas_pizza']['Name'], data.RawMaterial['Bundas_kenyer']['Name'],
                                     'Pizza feltét')
        self.productAssert.assertPizzaExists(data.Pizza['Sonkas_pizza']['Name'],
                                             data.Pizza['Sonkas_pizza']['GrossPrice'])
        self.productseed.deletePizza(data.Pizza['Sonkas_pizza']['Name'])

    @unittest.skip
    def testUpdate(self):
        modofiedName = 'Gumicukros pizza'
        modifiedNetPrice = 3000
        modifiedGrossPrice = self.html.extendedRound(modifiedNetPrice * 1.27, 2)

        self.productseed.createPizza(data.Pizza['Sonkas_pizza']['Name'], data.RawMaterial['Bundas_kenyer']['Name'], 'Pizza feltét')

        self.html.clickTableElement('customproduct-2', 'id', data.Pizza['Sonkas_pizza']['Name'], 'a', 'Szerkeszt', 'Pizza (testreszabható)')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', modofiedName)

        self.html.clickElement('Mennyiségek', 'a')
        # td = self.html.getElement('Eladási ár(ak)', 'td')
        self.html.clickElement('edit actionButton fright editPriceBtn', 'a', Options(htmlAttribute='class'))

        self.html.fillInput('Nettó', modifiedNetPrice)
        self.html.wait(2)
        self.html.clickElement('Rögzít', 'a', waitSeconds=2)
        #self.html.closeAllert()
        #self.html.clickElement('Rögzít', 'a')

        self.html.clickElement('Rögzít')
        self.html.refresh()

        self.productAssert.assertPizzaExists(modofiedName, modifiedGrossPrice)

        self.productseed.deletePizza(modofiedName)

    @unittest.skip
    def testWasting(self):
        self.productseed.createPizza(data.Pizza['Sonkas_pizza']['Name'], data.RawMaterial['Bundas_kenyer']['Name'], 'Pizza feltét')
        self.productAssert.assertPizzaExists(data.Pizza['Sonkas_pizza']['Name'], data.Pizza['Sonkas_pizza']['GrossPrice'])

        self.html.clickTableElement('customproduct-2', 'id', data.Pizza['Sonkas_pizza']['Name'], 'a', 'Selejt', 'Pizza (testreszabható)')
        self.html.switchFrame('iframe')

        time = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.html.fillInput('Selejt darabszám', data.Pizza['Sonkas_pizza']['WasteQuantity'], 'placeholder')
        self.html.clickElement('Minőségi kifogás')

        self.html.switchFrame()

        self.menu.openStatistics()

        self.html.clickElement('Termék selejtezések és sztornózások', 'a')

        self.html.clickElement('Mehet', waitSeconds=3)

        self.productAssert.assertWastingExists(data.Pizza['Sonkas_pizza']['Name'], time)

        self.menu.openProducts()
        self.html.clickElement('Pizza (testreszabható)', 'a')
        self.productseed.deletePizza(data.Pizza['Sonkas_pizza']['Name'])

    def testCreatePizza(self):
        self.productseed.createProduct(data.Product['Sonka']['Name'], data.Product['Sonka']['ProductGroup'],
                                       data.Product['Sonka']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Sonka']['Name'], data.Product['Sonka']['Quantity'],
                                       data.Product['Sonka']['NetPrice'],
                                       module=True)

        self.productseed.createProduct(data.Product['Paradicsomszósz']['Name'],
                                       data.Product['Paradicsomszósz']['ProductGroup'],
                                       data.Product['Paradicsomszósz']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Paradicsomszósz']['Name'],
                                       data.Product['Paradicsomszósz']['Quantity'], '0',
                                       module=True)
        self.productseed.createSpecialPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'],
                                            data.Product['Sonka']['Name'], module=True)

        self.productAssert.assertPizzaExists('Sonkás pizza', '1400.00')




