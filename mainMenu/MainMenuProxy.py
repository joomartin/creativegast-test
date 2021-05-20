from selenium.common.exceptions import NoSuchElementException

from core.HtmlProxy import HtmlProxy
import os
from dotenv import load_dotenv
load_dotenv()

class MainMenuProxy:

    def __init__(self, driver):
        self.driver = driver
        self.html = HtmlProxy(self.driver)
        self.baseUrl = os.environ.get('URL')

    def openRestaurant(self):
        self.navigate('restaurant/index')
        self.wait()
        try:
            self.html.clickElement('A műveletet elvégeztem')
        except:
            pass


    def openProducts(self):
        self.navigate('products')
        self.wait()

    def openStocks(self):
        self.navigate('warehouse')
        self.wait()

    def openReceiving(self):
        self.navigate('receiving')
        self.wait()

    def openStatistics(self):
        self.navigate('statistics/itemsale')
        self.wait()

    def openProduction(self):
        self.navigate('conveniences')
        self.wait()

    def openClientManagement(self):
        self.navigate('clients')
        self.wait()

    def openUsers(self):
        self.navigate('staff')
        self.wait()

    def openTableMapEditor(self):
        self.navigate('tablemapeditor/index')
        self.wait()

    def openFinance(self):
        self.navigate('finance')
        self.wait()

    def wait(self):
        self.html.wait()

    def navigate(self, destination):
        self.driver.get(self.baseUrl + '/' + destination)


