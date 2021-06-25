from datetime import datetime
import unittest

from selenium import webdriver
from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from seeders.ClientSeed import ClientSeed
from seeders.UsersSeed import UsersSeed
from stock.StockAssert import StockAssert
from products.ProductAssert import ProductAssert
from receiving.ReceivingAssert import ReceivingAssert
from restaurant.RestaurantAssert import RestaurantAssert
from clientManagement.ClientManagementAssert import ClientManagementAssert
from users.UsersAssert import UserAssert
from seeders.StockSeed import StockSeed
from seeders.ProductSeed import ProductSeed
from seeders.ReceivingSeed import ReceivingSeed
from seeders.RestaurantSeed import RestaurantSeed
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv
load_dotenv()


class BaseTestCase(unittest.TestCase):

    '''def run(self, result=None):
        super(BaseTestCase, self).run(result)
        if result.failures or result.errors:
            print('asdasdasdasdasdasdasdasdasdasdasd')
            self.html.screenshot('screenshot')'''

    def runTest(self, callback, name='screenshot'):
        try:
            callback()
        except Exception as e:
            self.html.screenshot(name)
            raise e

    @classmethod
    def setUpClass(self):
        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        #chrome_options.add_argument('--window-size=1920,1080')
        #chrome_options.add_argument("--auto-open-devtools-for-tabs")
        #chrome_options.add_argument('--disable-gpu')
        #chrome_options.headless = True
        self.driver = webdriver.Chrome(executable_path=os.environ.get('DRIVER'), options=chrome_options)

        self.driver.delete_all_cookies()
        self.driver.maximize_window()

        self.driver.get(os.environ.get('URL'))

        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.stockseed = StockSeed(self.driver)
        self.productseed = ProductSeed(self.driver)
        self.receivingseed = ReceivingSeed(self.driver)
        self.restaurantseed = RestaurantSeed(self.driver)
        self.clientseed = ClientSeed(self.driver)
        self.usersSeed = UsersSeed(self.driver)
        self.stockAssert = StockAssert(self.html, self.driver)
        self.productAssert = ProductAssert(self.html, self.driver)
        self.receivingAssert = ReceivingAssert(self.html, self.driver)
        self.restaurantAssert = RestaurantAssert(self.html, self.driver)
        self.clientAssert = ClientManagementAssert(self.html, self.driver)
        self.usersAssert = UserAssert(self.html, self.driver)
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
        self.html.fillInput('Felhasználónév', os.environ.get('USER_NAME'), selector='placeholder')
        self.html.fillInput('Jelszó', os.environ.get('USER_PASS'), selector='placeholder')

        self.html.clickElement('Belépés')
        self.html.fillInput('Belépési kód', os.environ.get('CODE'), selector='placeholder')
        self.html.clickElement('Belépés')








