from datetime import datetime
import unittest

#from selenium import webdriver
from seleniumwire import webdriver
from core.HtmlProxy import HtmlProxy
from core.Options import Options as op
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

    def runTest(self, callback, name='screenshot'):
        try:
            callback()
        except Exception as e:
            self.html.screenshot(name)
            with open("log_entries.txt", "wt") as out:
                out.write(self.driver.current_url + '\n')
                for request in self.driver.requests:
                    if request.response and request.response.status_code >= 400:
                        out.write('\ndate: %s \n' % request.date)
                        out.write('\nmethod: %s \n' % request.method)
                        out.write('\ncode: %s \n' % request.response.status_code)
                        out.write('\nheaders: %s' % request.response.headers)
                        out.write('\nresponse body: %s \n' % request.response.body)
                        out.write('\nrequest body: %s \n' % request.body)
                        out.write('\nurl: %s \n' % request.url)
                        out.write('\n\n')
                        out.write('___________________________________________________________________________________________')
                        out.write('\n\n\n')
            raise e

    def assertRange(self, expected, actual):
        self.assertTrue(expected - 1 <= actual <= expected + 1)

    @classmethod
    def setUpClass(self):
        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        #chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # chrome_options.add_argument("--auto-open-devtools-for-tabs")
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.headless = True
        self.driver = webdriver.Chrome(executable_path=os.environ.get('DRIVER'), options=chrome_options)

        self.driver.delete_all_cookies()
        self.driver.maximize_window()

        hosts = os.environ.get('ALLOWED_HOSTS')
        if os.environ.get('URL') not in hosts:
            raise Exception('A host nem engedélyezett!')

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

    def login(self):
        self.html.fillInput('Felhasználónév', os.environ.get('USER_NAME'), selector='placeholder')
        self.html.fillInput('Jelszó', os.environ.get('USER_PASS'), selector='placeholder')

        self.html.clickElement('Belépés')
        self.html.fillInput('Belépési kód', os.environ.get('CODE'), selector='placeholder')
        self.html.clickElement('Belépés', waitSeconds=2)

        # napnyitas
        try:
            self.html.getElement('Kérjük zárjon napot!', 'span')
            self.menu.openFinance()
            self.html.clickElement('Helyiségek zárása', waitSeconds=2)
            self.html.clickElement('Igen')
            self.html.fillInput('Belépő kód:', os.environ.get('USER_PASS'))
            self.html.wait(1)
            self.html.clickElement('sendClosePasswordBtn', 'button', options=op(htmlAttribute='id'))
            self.html.explicitWaitXpath('/html/body/section/div/a[1]')
            self.menu.openRestaurant()
            self.html.clickElement('Étterem nyitása', waitSeconds=2)
            self.menu.openRestaurant()
            self.html.clickElement('Dinamikus futár asztalok', 'a')
            self.html.clickElement('Dinamikus futár asztalok nyitása', waitSeconds=2)
            self.menu.openRestaurant()
            self.html.clickElement('Törzsvendégek', 'a')
            self.html.clickElement('Törzsvendégek nyitása', waitSeconds=2)
        except Exception as e:
            pass
