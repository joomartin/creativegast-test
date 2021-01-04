import unittest

from selenium import webdriver
from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from stock.StockAssert import StockAssert
from products.ProductAssert import ProductAssert
from receiving.ReceivingAssert import ReceivingAssert
from Config import read_section
from seeders.StockSeed import StockSeed
from seeders.ProductSeed import ProductSeed
from seeders.ReceivingSeed import ReceivingSeed

class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = webdriver.Chrome(executable_path='C:/webdrivers/chromedriver.exe')
        #self.driver = webdriver.Firefox(executable_path='C:/webdrivers/geckodriver.exe')
        self.driver.maximize_window()

        config = read_section()
        self.driver.get(config.get('path'))

        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.stockseed = StockSeed(self.driver)
        self.productseed = ProductSeed(self.driver)
        self.receivingseed= ReceivingSeed(self.driver)
        self.stockAssert = StockAssert(self.html,self.driver)
        self.productAssert = ProductAssert(self.html,self.driver)
        self.receivingAssert=ReceivingAssert(self.html,self.driver)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def login(self):
        self.html.fillInput('Felhasználónév', 'admin', selector='placeholder')
        self.html.fillInput('Jelszó', 'admin', selector='placeholder')

        self.html.clickElement('Belépés')
        self.html.fillInput('Belépési kód', 'admin', selector='placeholder')
        self.html.clickElement('Belépés')








