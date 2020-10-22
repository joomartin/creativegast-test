import unittest

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from core.HtmlProxy import HtmlProxy
from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy
from stock.StockAssert import StockAssert
from Config import read_section
from shared.BaseTestCase import BaseTestCase


class StockMovement(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openStocks()
        self.html.clickElement('Raktármozgás', 'a')

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def createNewMovement(self):
        self.html.wait()
        self.html.clickElement('Új raktármozgás', 'a', waitSeconds=2)
        self.html.clickElement('Új')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Forrás raktár','Pult')
        self.html.wait()
        self.html.clickDropdown('Cél raktár', 'Konyha')

        self.html.fillAutocomplete('Nyersanyag', 'input', 'Coca','Coca Cola 025l', 'li', Options(htmlAttribute='data-title'))
        self.html.getElement('Maximum', 'input', Options(htmlAttribute='data-title')).click()
        self.html.wait()
        self.html.fillInput('Mennyiség', '11', 'data-title')
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()

        #self.html.clickElement('Admin Admin admin', 'td[@class="sorting_1"]', Options(following='a'))


    def testCreate(self):
        self.createNewMovement()
