from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options
from selenium.webdriver.common.action_chains import ActionChains
from restaurant.Restaurant import Restaurant


class Menus(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)


    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def testMenus(self):

        self.menu.openRestaurant()
        self.html.wait(2)
        self.html.getElement('Étterem', 'a')

        self.menu.openProducts()
        self.html.wait(2)
        self.html.getElement('Termékek', 'a')

        self.menu.openStocks()
        self.html.wait(2)
        self.html.getElement('Raktárkészlet', 'a')

        self.menu.openReceiving()
        self.html.wait(2)
        self.html.getElement('Bevételezés', 'a')

        self.menu.openProduction()
        self.html.wait(2)
        self.html.getElement('Gyártás', 'a')

        self.menu.openStatistics()
        self.html.wait(2)
        self.html.getElement('Keresési feltételek', 'a')

        self.menu.openFinance()
        self.html.wait(2)
        self.html.getElement('Egyenleg', 'a')

        self.menu.openUsers()
        self.html.wait(2)
        self.html.getElement('Személyzet', 'a')

        self.menu.openTableMapEditor()
        self.html.wait(2)
        self.html.getElement('Étterem', 'a')


