import unittest

from selenium.common.exceptions import NoSuchElementException
from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy
from core.CGSpecific import CGSpecific as cg


class RestaurantAssert(unittest.TestCase):

    def __init__(self, htmlProxy, driver):
        super().__init__()
        self.html = htmlProxy
        self.menu = MainMenuProxy(driver)
        self.cg = cg()

    def assertTableExists(self, tableName):
        self.assertTrue(self.html.getElement(tableName, 'i').is_displayed())

    def assertProductNotInList(self):
        self.assertFalse(self.html.getElement('Fizetés', 'button').is_displayed())

    def assertStornoSucces(self, name):
        self.html.wait(5)
        self.assertTrue(self.html.getElement(name + ' nevű termék a felszolgáló által sztornózva lett! ', 'li').is_displayed())
        self.html.clickElement('Rendben', 'a')

    def assertProductInList(self):
        pass




