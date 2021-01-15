
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
        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['GrossPrice'], data.RawMaterial['Bundas_kenyer']['Quantity'], data.WareHouses['Szeszraktár']['Name'], data.RawMaterial['Bundas_kenyer']['ME'], module=True)
        #self.stockseed.createRawMaterial('Pizza feltét', '500', '100', 'Pizzatest', 'db')

        self.menu.openProducts()
        self.html.clickElement('Pizza (testreszabható)', 'a')

    @classmethod
    def tearDownClass(self):
        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)
        super().tearDownClass()
        pass


    def testCreate(self):
        testName = 'Create pizza'
        self.productseed.createPizza(data.Pizza['Sonkas_pizza']['Name'], data.RawMaterial['Bundas_kenyer']['Name'], 'Pizza feltét')
        self.productAssert.assertPizzaExists(data.Pizza['Sonkas_pizza']['Name'], data.Pizza['Sonkas_pizza']['GrossPrice'])
        self.productseed.deletePizza(data.Pizza['Sonkas_pizza']['Name'])


    def testUpdate(self):
        modofiedName = 'Gumicukros pizza'
        modifiedNetPrice = 3000
        extended_round = lambda x, n: eval('"%.' + str(int(n)) + 'f" % ' + repr(x))
        modifiedGrossPrice = self.html.extendedRound(modifiedNetPrice * 1.27, 2)

        self.productseed.createPizza(data.Pizza['Sonkas_pizza']['Name'], data.RawMaterial['Bundas_kenyer']['Name'], 'Pizza feltét')

        self.html.clickTableElement('customproduct-2', 'id', data.Pizza['Sonkas_pizza']['Name'], 'a', 'Szerkeszt', 'Pizza (testreszabható)')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', modofiedName)

        self.html.clickElement('Mennyiségek', 'a')
        # td = self.html.getElement('Eladási ár(ak)', 'td')
        self.html.clickElement('edit actionButton fright editPriceBtn', 'a', Options(htmlAttribute='class'))

        self.html.fillInput('Nettó', modifiedNetPrice)
        self.html.clickElement('Rögzít', 'a', waitSeconds=2)
        self.html.closeAllert()
        self.html.clickElement('Rögzít', 'a')

        self.html.clickElement('Rögzít')
        self.html.refresh()

        self.productAssert.assertPizzaExists(modofiedName, modifiedGrossPrice)

        self.productseed.deletePizza(modofiedName)


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

