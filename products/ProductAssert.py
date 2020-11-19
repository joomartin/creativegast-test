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

    def assertCounterExists(self, name, tab):
        self.html.search(name, tab)
        self.assertTrue(self.html.getElement(name, 'td').is_displayed())
        self.html.search('', tab)

    def assertCounterNotExists(self, name, tab):
        with self.assertRaises(NoSuchElementException):
            self.html.getElementInTable(name, 'counters', tab)

    def assertProductExist(self, name, tab):
        self.html.search(name, tab)
        self.assertTrue(self.html.getElement(name, 'td').is_displayed())
        self.html.search('', tab)

    def assertProductElementExist(self, element):
        self.assertTrue(self.html.getElement(element, 'td').is_displayed())

    def assertPizzaExists(self, pizzaName, price):
        self.html.search(pizzaName, 'Pizza (testreszabható)')
        self.assertTrue(self.html.getElement(pizzaName, 'td').is_displayed())
        dispPrice = self.html.getElement(pizzaName, 'td', Options(following='td[4]')).text
        self.assertEqual(dispPrice,price)

    def assertWastingExists(self, pizzaName, time):
        exists = self.html.getElement(pizzaName, 'td').is_displayed() and self.html.getElement(time, 'td').is_displayed()
        self.assertTrue(exists)

