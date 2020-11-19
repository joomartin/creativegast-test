from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from datetime import datetime


class Pizza(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.stockseed.createWarehouse('PizzaTest')
        self.stockseed.createRawMaterialWithOpening('Pizza tészta', '1000', '10', 'PizzaTest', 'db')
        #self.stockseed.createRawMaterial('Pizza feltét', '500', '100', 'Pizzatest', 'db')

        self.menu.openProducts()
        self.html.clickElement('Pizza (testreszabható)', 'a')

    @classmethod
    def tearDownClass(self):
        self.stockseed.deleteRawMaterial('Pizza tészta')
        self.stockseed.deleteWarehouse('PizzaTest')
        super().tearDownClass()


    def testCreate(self):
        testName = 'Create pizza'
        self.productseed.createPizza(testName, 'Pizza tészta', 'Pizza feltét')
        self.productAssert.assertPizzaExists(testName,'1 270.00')
        self.productseed.deletePizza(testName)

    def testUpdate(self):
        testName = 'Update pizza'
        newName = 'Uj pizza'

        self.productseed.createPizza(testName, 'Pizza tészta', 'Pizza feltét')

        self.html.clickTableElement('customproduct-2', 'id', testName, 'a', 'Szerkeszt', 'Pizza (testreszabható)')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', newName)

        self.html.clickElement('Mennyiségek', 'a')
        td = self.html.getElement('Eladási ár(ak)', 'td')
        self.html.clickElement('edit actionButton fright editPriceBtn', 'a', Options(htmlAttribute='class'))

        self.html.fillInput('Nettó', '3000')
        self.html.clickElement('Rögzít', 'a')
        self.html.closeAllert()
        self.html.clickElement('Rögzít', 'a')

        self.html.clickElement('Rögzít')

        self.productAssert.assertPizzaExists(newName, '3 810.00')

        self.productseed.deletePizza(newName)

    def testWasting(self):
        testName = 'Waste pizza'

        self.productseed.createPizza(testName, 'Pizza tészta', 'Pizza feltét')
        self.productAssert.assertPizzaExists(testName, '1 270.00')

        self.html.clickTableElement('customproduct-2', 'id', testName, 'a', 'Selejt', 'Pizza (testreszabható)')
        self.html.switchFrame('iframe')

        time = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.html.fillInput('Selejt darabszám', '10', 'placeholder')
        self.html.clickElement('Minőségi kifogás')

        self.html.switchFrame()

        self.menu.openStatistics()

        self.html.clickElement('Termék selejtezések és sztornózások', 'a')

        self.html.clickElement('Mehet', waitSeconds=3)

        self.productAssert.assertWastingExists(testName, time)

        self.menu.openProducts()
        self.html.clickElement('Pizza (testreszabható)', 'a')
        self.productseed.deletePizza(testName)

