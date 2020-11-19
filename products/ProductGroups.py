import unittest

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from core.HtmlProxy import HtmlProxy
from core.Options import Options
from mainMenu.MainMenuProxy import MainMenuProxy
from products.ProductAssert import ProductAssert
from stock.StockAssert import StockAssert
from Config import read_section
from shared.BaseTestCase import BaseTestCase


class ProductGroups(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openProducts()
        self.html.clickTab('Termékcsoportok')

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()


    def testCreate(self):
        testName = 'testGroup'
        self.productseed.createProductGroup(testName)
        self.html.search(testName,'Termékcsoportok')
        self.productAssert.assertGroupExists(testName)
        self.productseed.deleteProductGroup(testName)


    def testCreateWithParentGroup(self):
        testName = 'testGroupWithParent'
        self.html.clickElement('Új termékcsoport felvitele', 'a')

        self.html.switchFrame('iframe')

        self.html.fillInput('Termékcsoport neve', testName)
        self.html.clickDropdown('Kategória', 'Étel')
        self.html.clickElement('Ételek', 'a')
        self.html.clickElement('Rögzít')
        self.html.wait(5)

        self.html.switchFrame()

        self.productAssert.asseretParentGroup(testName, 'Ételek')

        self.productseed.deleteProductGroup(testName)

    def testUpdateGroup(self):
        testName = 'testGroup'
        newName = 'modifiedName'
        self.productseed.createProductGroup(testName)
        self.html.search(testName, 'Termékcsoportok')
        self.productAssert.assertGroupExists(testName)
        self.html.clickTableElement('product_groups', 'id', testName, 'span', 'Szerkeszt', 'Termékcsoportok')

        self.html.switchFrame('iframe')

        self.html.fillInput('Termékcsoport neve', newName)
        self.html.clickElement('Rögzít')
        self.html.wait(3)
        self.html.switchFrame()
        self.html.refresh()
        self.html.search(newName, 'Termékcsoportok')
        self.productAssert.assertGroupExists(newName)

        self.productseed.deleteProductGroup(newName)