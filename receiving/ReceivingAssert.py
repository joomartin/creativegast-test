import unittest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy


class ReceivingAssert(unittest.TestCase):

    def __init__(self, htmlProxy, driver):
        super().__init__()
        self.html = htmlProxy
        self.menu = MainMenuProxy(driver)

    def assertPartnerExist(self, name, tab):
        self.assertTrue(self.html.getElementInTable(name, 'partners', tab).is_displayed())

    def assertPartnerNotExist(self, name, tab):
        with self.assertRaises(NoSuchElementException):
            self.html.getElementInTable(name, 'partners', tab)

    def assertReceivingExists(self, partnerName):
        self.html.clickElement('Keresés')
        self.html.wait(2)
        self.assertTrue(self.html.getElement(partnerName, 'td').is_displayed())

    def assertReceivingDetails(self, materialName, qty,):

        table = self.html.getElement('noHover', 'table', options=Options(htmlAttribute='class'))
        name=self.html.getElement(materialName, 'td', Options(element=table)).text
        self.assertEqual(name,materialName)

        actqty=self.html.getElement(materialName, 'td', Options(following='td', element=table)).text
        self.assertEqual(actqty,qty)