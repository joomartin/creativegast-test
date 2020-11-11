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

        self.menu.openProducts()
        self.html.clickElement('Pizza (testreszabható)', 'a')

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def createPizza(self, pizzaName):
        self.html.clickElement('Új pizza (testreszabható)', 'a')

        self.html.switchFrame('iframe')
        self.html.clickDropdown('Nyomtatási részleg', 'Pizza')
        self.html.fillInput('Termék neve', pizzaName)
        self.html.fillInput('Kód', '1211')

        self.html.clickDropdown('Szósz', 'Paradicsomos alap')

        self.html.fillAutocomplete('baseComponentName', 'input', 'liszt', 'Liszt (teszt)', 'li', Options(htmlAttribute='id'))
        table = self.html.getElement('baseComponents', 'table', Options(htmlAttribute='id'))
        self.html.getElement('Hozzáad', 'button', element=table).click()


        self.html.fillAutocomplete('toppingComponentName', 'input', 'Sonka', 'Sonka Feltét', 'li', Options(htmlAttribute='id'))
        table = self.html.getElement('toppingComponents', 'table', Options(htmlAttribute='id'))
        self.html.getElement('Hozzáad', 'button', element=table).click()

        self.html.clickElement('Mennyiségek', 'a')
        self.html.wait(2)
        td = self.html.getElement('Eladási ár(ak)', 'td')
        self.html.clickElement('edit actionButton fright editPriceBtn', 'a', Options(htmlAttribute='class'))

        self.html.fillInput('Nettó', '1000')
        self.html.clickElement('Rögzít', 'a')
        self.html.closeAllert()
        self.html.clickElement('Rögzít', 'a')
        self.html.wait(2)
        self.html.clickElement('Rögzít')


    def deletePizza(self, pizzaName):
        self.html.clickTableElement('customproduct-2', 'id', pizzaName, 'a', 'Törlés', 'Pizza (testreszabható)')
        self.html.clickElement('Igen')


    def testCreate(self):
        testName = 'Create pizza'
        self.createPizza(testName)
        self.productAssert.assertPizzaExists(testName,'1 270.00')
        self.deletePizza(testName)

    def testUpdate(self):
        testName = 'Update pizza'
        newName = 'Uj pizza'

        self.createPizza(testName)

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

        self.deletePizza(newName)

    def testWasting(self):
        testName = 'Waste pizza'

        self.createPizza(testName)
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
        self.deletePizza(testName)

