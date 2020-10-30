import unittest

from selenium import webdriver
from core.HtmlProxy import HtmlProxy
from mainMenu.MainMenuProxy import MainMenuProxy
from stock.StockAssert import StockAssert
from Config import read_section

class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = webdriver.Chrome(executable_path='C:/webdrivers/chromedriver.exe')
        self.driver.maximize_window()

        config = read_section()
        self.driver.get(config.get('path'))

        self.html = HtmlProxy(self.driver)
        self.menu = MainMenuProxy(self.driver)
        self.stockAssert = StockAssert(self.html)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def login(self):
        self.html.fillInput('Felhasználónév', 'admin', selector='placeholder')
        self.html.fillInput('Jelszó', 'admin', selector='placeholder')

        self.html.clickElement('Belépés')
        self.html.fillInput('Belépési kód', 'admin', selector='placeholder')
        self.html.clickElement('Belépés')








