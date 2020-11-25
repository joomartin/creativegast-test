import unittest

from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as td

class Test(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openStocks()
        self.html.clickElement('Raktárak', 'a')

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()



    def testCreateWarehouse(self):
        self.stockseed.createWarehouse(td.WareHouse['Name'])
        self.stockAssert.assertWarehouseExist(td.WareHouse['Name'], 'Raktárak')
        self.html.search('', 'Raktárak')

        self.stockseed.deleteWarehouse(td.WareHouse['Name'])

    #@unittest.skip
    def testCantCreate(self):
        self.stockseed.createWarehouse(td.WareHouse['Name'])
        self.html.clickElement('Új raktár felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Raktár neve', td.WareHouse['Name'])
        self.html.clickElement('Rögzít')

        self.stockAssert.assertDialogDisplayed()

        self.html.clearInput('Raktár neve')
        self.html.clickElement('Mégsem')

        self.stockseed.deleteWarehouse(td.WareHouse['Name'])

    #@unittest.skip
    def testEdit(self):
        self.stockseed.createWarehouse(td.WareHouse['Name'])
        self.html.clickElement(None,
                               "//tr[contains(., " + td.WareHouse['Name'] + ")]//a[contains(@class, 'edit') and contains(@class, 'actionButton')]",
                               Options(uniqueSelector=True))

        self.html.switchFrame('iframe')
        self.html.fillInput('Raktár neve', td.WareHouse2['Name'])
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()

        self.stockAssert.assertWarehouseExist(td.WareHouse2['Name'], 'Raktárak')
        self.html.search('', 'Raktárak')

        self.stockseed.deleteWarehouse(td.WareHouse2['Name'])


    def testDelete(self):
        self.html.refresh()
        self.stockseed.createWarehouse(td.WareHouse['Name'])
        self.html.search(td.WareHouse['Name'], 'Raktárak')
        currWindow = self.html.getElement('tabs-3', 'div', options=Options(htmlAttribute='id'))
        self.html.clickElement(td.WareHouse['Name'], 'td', Options(following='a'), element = currWindow)
        self.html.clickElement("Igen", waitSeconds=2)
        self.html.search('', 'Raktárak')

        self.stockAssert.assertWarehouseNotExist(td.WareHouse['Name'], 'Raktárak')
        self.html.search('', 'Raktárak')


if __name__ == "__main__":
    unittest.main()
