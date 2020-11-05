import unittest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy


class ProductAssert(unittest.TestCase):

    def __init__(self, htmlProxy, driver):
        super().__init__()
        self.html = htmlProxy
        self.menu = MainMenuProxy(driver)

    def assertGroupExists(self,name):
        self.assertTrue(self.html.getElement(name, 'td').is_displayed())

    def asseretParentGroup(self, groupName, parentName):
        parent = self.html.getElement(groupName, 'td', Options(following='td')).text
        self.assertEqual(parent, parentName)

    def assertMenuExists(self, menuName, price):
        dispPrice = self.html.getElement(menuName, 'td', Options(following='td[3]')).text
        self.assertEqual(price, dispPrice)

    def assertDialogDisplayed(self):
        self.assertTrue(self.html.getElement('iframe', 'body', Options(htmlAttribute='class')).is_displayed())