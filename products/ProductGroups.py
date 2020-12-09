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
from shared.TestData import TestData as td


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
        testName = td.ProductGroup['Name']
        self.productseed.createProductGroup(testName)
        self.html.search(testName,'Termékcsoportok')
        self.productAssert.assertGroupExists(testName)
        self.productseed.deleteProductGroup(testName)


    def testCreateWithParentGroup(self):
        testName = td.ProductGroup['Name']
        self.html.clickElement('Új termékcsoport felvitele', 'a')

        self.html.switchFrame('iframe')

        self.html.fillInput('Termékcsoport neve', testName)
        self.html.clickDropdown('Kategória', 'Étel')
        self.html.clickElement('Ételek', 'a')
        self.html.clickElement('Rögzít')
        self.html.wait(5)

        self.html.switchFrame()
        self.html.wait(8)
        self.productAssert.asseretParentGroup(testName, 'Ételek')

        self.productseed.deleteProductGroup(testName, module=True)

    def testUpdateGroup(self):
        testName = td.ProductGroup['Name']
        newName = td.ProductGroup['ModifiedName']
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