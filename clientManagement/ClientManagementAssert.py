import unittest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy


class ClientManagementAssert(unittest.TestCase):

    def __init__(self, htmlProxy, driver):
        super().__init__()
        self.html = htmlProxy
        self.menu = MainMenuProxy(driver)

    def assertClientExist(self, name, address, phone, discount, code):
        self.html.search(name, 'Törzsvendégek')
        self.html.clickTableElement('frequenters', 'id', name, 'a', 'Részletek')
        self.html.switchFrame('iframe')
        #name = self.html.getElement('cl_name', 'input', options=Options(htmlAttribute='id'))
        self.assertTrue(self.html.getTablePairsExist('Név', name))
        self.assertTrue(self.html.getTablePairsExist('Cím', address))
        self.assertTrue(self.html.getTablePairsExist('Telefon', phone))
        self.assertTrue(self.html.getTablePairsExist('Kedv.', discount))
        self.assertTrue(self.html.getTablePairsExist('Kód', code))

        self.html.switchFrame()
        self.html.clickElement('fancybox-item fancybox-close', 'a', options=Options(htmlAttribute='class'))





























