from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from datetime import datetime
from shared.TestData import TestData as data

class Pizza(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['GrosPrice'], data.RawMaterial['Bundas_kenyer']['Quantity'], data.WareHouses['Szeszraktár']['Name'], data.RawMaterial['Bundas_kenyer']['ME'], module=True)
        #self.stockseed.createRawMaterial('Pizza feltét', '500', '100', 'Pizzatest', 'db')

        self.menu.openProducts()
        self.html.clickElement('Pizza (testreszabható)', 'a')

    @classmethod
    def tearDownClass(self):
        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)
        super().tearDownClass()

    '''
    def testCreate(self):
        testName = 'Create pizza'
        self.productseed.createPizza(td.Pizza['Name'], td.RawMaterial['Name'], 'Pizza feltét')
        self.productAssert.assertPizzaExists(td.Pizza['Name'], td.Pizza['GrossPrice'])
        self.productseed.deletePizza(td.Pizza['Name'])
    '''

    def testUpdate(self):
        testName = 'Update pizza'
        newName = 'Uj pizza'

        self.productseed.createPizza(data.Pizza['Sonkas_pizza']['Name'], data.RawMaterial['Bundas_kenyer']['Name'], 'Pizza feltét')

        self.html.clickTableElement('customproduct-2', 'id', data.Pizza['Sonkas_pizza']['Name'], 'a', 'Szerkeszt', 'Pizza (testreszabható)')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', data.Pizza['Sonkas_pizza']['ModifiedName'])

        self.html.clickElement('Mennyiségek', 'a')
        # td = self.html.getElement('Eladási ár(ak)', 'td')
        self.html.clickElement('edit actionButton fright editPriceBtn', 'a', Options(htmlAttribute='class'))

        self.html.fillInput('Nettó', data.Pizza['Sonkas_pizza']['ModifiedNetPrice'])
        self.html.clickElement('Rögzít', 'a')
        self.html.closeAllert()
        self.html.clickElement('Rögzít', 'a')

        self.html.clickElement('Rögzít')
        self.html.refresh()

        self.productAssert.assertPizzaExists(data.Pizza['Sonkas_pizza']['ModifiedName'], data.Pizza['Sonkas_pizza']['ModifiedGrossPrice'])

        self.productseed.deletePizza(data.Pizza['Sonkas_pizza']['ModifiedName'])

    def testWasting(self):
        testName = 'Waste pizza'

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

