
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
        testName = td.ProductGroup['Egyeb']['Name']
        self.productseed.createProductGroup(testName)
        self.html.search(testName, 'Termékcsoportok')
        self.productAssert.assertGroupExists(testName)
        self.productseed.deleteProductGroup(testName)

    '''
    def testCreateWithParentGroup(self):
        testName = td.ProductGroup['Egyeb']['Name']
        self.html.clickElement('Új termékcsoport felvitele', 'a')

        self.html.switchFrame('iframe')

        self.html.fillInput('Termékcsoport neve', testName)
        self.html.clickDropdown('Kategória', 'Étel')
        self.html.clickElement('Ételek', 'a')
        self.html.clickElement('Rögzít')
        #self.html.wait(5)
        self.driver.implicitly_wait(100000)

        self.html.switchFrame()
        self.html.wait(8000)
        self.productAssert.asseretParentGroup(testName, 'Ételek')

        self.productseed.deleteProductGroup(testName, module=True)
    '''

    def testUpdateGroup(self):
        testName = td.ProductGroup['Egyeb']['Name']
        modifiedName = 'egzotikus fuszerek'

        self.productseed.createProductGroup(testName)
        self.html.search(testName, 'Termékcsoportok')
        self.productAssert.assertGroupExists(testName)
        self.html.clickTableElement('product_groups', 'id', testName, 'span', 'Szerkeszt', 'Termékcsoportok')

        self.html.switchFrame('iframe')

        self.html.fillInput('Termékcsoport neve', modifiedName)
        self.html.clickElement('Rögzít')
        self.html.wait(3)
        self.html.switchFrame()
        self.html.refresh()
        self.html.search(modifiedName, 'Termékcsoportok')
        self.productAssert.assertGroupExists(modifiedName)

        self.productseed.deleteProductGroup(modifiedName)
