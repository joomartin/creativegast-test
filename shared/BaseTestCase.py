from datetime import datetime
import unittest

from selenium import webdriver
from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from stock.StockAssert import StockAssert
from products.ProductAssert import ProductAssert
from receiving.ReceivingAssert import ReceivingAssert
from restaurant.RestaurantAssert import RestaurantAssert
from Config import read_section
from seeders.StockSeed import StockSeed
from seeders.ProductSeed import ProductSeed
from seeders.ReceivingSeed import ReceivingSeed
from seeders.RestaurantSeed import RestaurantSeed
from selenium.webdriver.chrome.options import Options


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        chrome_options = Options()
        # chrome_options.add_argument("--auto-open-devtools-for-tabs")
        self.driver = webdriver.Chrome(executable_path='C:/webdrivers/chromedriver.exe', options=chrome_options)

        self.driver.delete_all_cookies()
        self.driver.maximize_window()

        config = read_section()
        self.driver.get(config.get('path'))

        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.stockseed = StockSeed(self.driver)
        self.productseed = ProductSeed(self.driver)
        self.receivingseed= ReceivingSeed(self.driver)
        self.restaurantseed = RestaurantSeed(self.driver)
        self.stockAssert = StockAssert(self.html,self.driver)
        self.productAssert = ProductAssert(self.html,self.driver)
        self.receivingAssert=ReceivingAssert(self.html,self.driver)
        self.restaurantAssert=RestaurantAssert(self.html,self.driver)
        self.result = unittest.TestResult

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    '''
    @classmethod
    def tearDown(self):
        print('kint')
        # if not unittest.TestResult.wasSuccessful(unittest.TestResult()):
        print(self.defaultTestResult(self).errors)
        print('error:')
        print(len(self.result().errors))
        print('fail:')
        print(len(self.result().failures))
        if not len(self.result(self).errors) == 0:
            print('bent')
            now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            name = 'screenshot-%s.png' % now
            self.driver.save_screenshot(name)
            print(name)
    '''

    def login(self):
        self.html.fillInput('Felhasználónév', 'admin', selector='placeholder')
        self.html.fillInput('Jelszó', 'admin', selector='placeholder')

        self.html.clickElement('Belépés')
        self.html.fillInput('Belépési kód', 'admin', selector='placeholder')
        self.html.clickElement('Belépés')








