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

    def createProductGroup(self, groupName):
        self.html.clickElement('Új termékcsoport felvitele', 'a')

        self.html.switchFrame('iframe')

        self.html.fillInput('Termékcsoport neve', groupName)
        self.html.clickDropdown('Kategória', 'Étel')
        self.html.clickElement('Rögzít')
        self.html.switchFrame()
        self.html.wait(2)

    def deleteProductGroup(self, groupName):
        self.html.clickTableElement('product_groups', 'id', groupName, 'span', 'Törlés', 'Termékcsoportok')
        self.html.wait(2)
        self.html.clickElement('Igen')

    def testCreate(self):
        testName = 'testGroup'
        self.createProductGroup(testName)
        self.html.search(testName,'Termékcsoportok')
        self.productAssert.assertGroupExists(testName)
        self.deleteProductGroup(testName)


    def testCreateWithParentGroup(self):
        pass
        '''
        testName = 'testGroupWithParent'
        self.html.clickElement('Új termékcsoport felvitele', 'a')

        self.html.switchFrame('iframe')

        self.html.fillInput('Termékcsoport neve', testName)
        self.html.clickDropdown('Kategória', 'Étel')
        self.html.clickElement('Ételek', 'a')
        self.html.clickElement('Rögzít')

        self.html.switchFrame()

        self.productAssert.asseretParentGroup(testName, 'Ételek')

        self.deleteProductGroup(testName)
        '''

    def testUpdateGroup(self):
        testName = 'testGroup'
        newName = 'modifiedName'
        self.createProductGroup(testName)
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

        self.deleteProductGroup(newName)