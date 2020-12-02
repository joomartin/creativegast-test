from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from datetime import datetime
from shared.TestData import TestData as td

class Pizza(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.stockseed.createWarehouse(td.WareHouse['Name'])
        self.stockseed.createRawMaterialWithOpening(td.RawMaterial['Name'], td.RawMaterial['GrosPrice'], td.RawMaterial['Quantity'], td.WareHouse['Name'], td.RawMaterial['ME'])
        #self.stockseed.createRawMaterial('Pizza feltét', '500', '100', 'Pizzatest', 'db')

        self.menu.openProducts()
        self.html.clickElement('Pizza (testreszabható)', 'a')

    @classmethod
    def tearDownClass(self):
        self.stockseed.deleteRawMaterial(td.RawMaterial['Name'])
        self.stockseed.deleteWarehouse(td.WareHouse['Name'])
        super().tearDownClass()


    def testCreate(self):
        testName = 'Create pizza'
        self.productseed.createPizza(td.Pizza['Name'], td.RawMaterial['Name'], 'Pizza feltét')
        self.productAssert.assertPizzaExists(td.Pizza['Name'], td.Pizza['GrossPrice'])
        self.productseed.deletePizza(td.Pizza['Name'])

    def testUpdate(self):
        testName = 'Update pizza'
        newName = 'Uj pizza'

        self.productseed.createPizza(td.Pizza['Name'], td.RawMaterial['Name'], 'Pizza feltét')

        self.html.clickTableElement('customproduct-2', 'id', td.Pizza['Name'], 'a', 'Szerkeszt', 'Pizza (testreszabható)')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', td.Pizza['ModifiedName'])

        self.html.clickElement('Mennyiségek', 'a')
        # td = self.html.getElement('Eladási ár(ak)', 'td')
        self.html.clickElement('edit actionButton fright editPriceBtn', 'a', Options(htmlAttribute='class'))

        self.html.fillInput('Nettó', td.Pizza['ModifiedNetPrice'])
        self.html.clickElement('Rögzít', 'a')
        self.html.closeAllert()
        self.html.clickElement('Rögzít', 'a')

        self.html.clickElement('Rögzít')

        self.productAssert.assertPizzaExists(td.Pizza['ModifiedName'], td.Pizza['ModifiedGrossPrice'])

        self.productseed.deletePizza(td.Pizza['ModifiedName'])

    def testWasting(self):
        testName = 'Waste pizza'

        self.productseed.createPizza(td.Pizza['Name'], td.RawMaterial['Name'], 'Pizza feltét')
        self.productAssert.assertPizzaExists(td.Pizza['Name'], td.Pizza['GrossPrice'])

        self.html.clickTableElement('customproduct-2', 'id', td.Pizza['Name'], 'a', 'Selejt', 'Pizza (testreszabható)')
        self.html.switchFrame('iframe')

        time = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.html.fillInput('Selejt darabszám', td.Pizza['WasteQuantity'], 'placeholder')
        self.html.clickElement('Minőségi kifogás')

        self.html.switchFrame()

        self.menu.openStatistics()

        self.html.clickElement('Termék selejtezések és sztornózások', 'a')

        self.html.clickElement('Mehet', waitSeconds=3)

        self.productAssert.assertWastingExists(td.Pizza['Name'], time)

        self.menu.openProducts()
        self.html.clickElement('Pizza (testreszabható)', 'a')
        self.productseed.deletePizza(td.Pizza['Name'])

