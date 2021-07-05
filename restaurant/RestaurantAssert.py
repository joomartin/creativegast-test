import unittest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy
from core.CGSpecific import CGSpecific as cg


class RestaurantAssert(unittest.TestCase):

    def __init__(self, htmlProxy, driver):
        super().__init__()
        self.html = htmlProxy
        self.menu = MainMenuProxy(driver)
        self.driver = driver
        self.cg = cg()

    def assertTableExists(self, tableName):
        self.assertTrue(self.html.getElement(tableName, 'i').is_displayed())

    def assertProductNotInList(self):
        self.assertFalse(self.html.getElement('Fizetés', 'button').is_displayed())

    def assertStornoSucces(self, name):
        self.html.explicitWaitXpath(
            './/li[contains(., "' + name + ' nevű termék a felszolgáló által sztornózva lett!")]', mode='visible')
        self.html.clickElement('Rendben', 'a')

    def assertProductInList(self):
        pass




