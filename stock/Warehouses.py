import unittest

from core.Options import Options
from shared.BaseTestCase import BaseTestCase


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

    def createWarehouse(self, warehouseName):
        self.html.clickElement('Új raktár felvitele', 'a')
        self.html.switchFrame("iframe")

        self.html.fillInput('Raktár neve', warehouseName)
        self.html.clickElement("Rögzít")
        self.html.switchFrame()
        self.html.refresh()

    def deleteWarehouse(self, warehouseName):
        self.html.wait(2)
        self.html.clickElement(warehouseName, 'td[@class="sorting_1"]', Options(following='a'))
        self.html.clickElement('Igen')

    def testCreateWarehouse(self):
        self.createWarehouse("1newWH")
        self.stockAssert.assertWarehouseExist('1newWH')

        self.deleteWarehouse("1newWH")

    def testCantCreate(self):
        self.createWarehouse("2newWH")
        self.html.clickElement('Új raktár felvitele', 'a')
        self.html.switchFrame("iframe")

        self.html.fillInput('Raktár neve', '2newWH', )
        self.html.clickElement("Rögzít")

        self.stockAssert.assertDialogDisplayed()

        self.html.clearInput('Raktár neve')
        self.html.clickElement("Mégsem")

        self.deleteWarehouse("2newWH")

    def testEdit(self):
        self.createWarehouse("3newWH")
        self.html.clickElement(None,
                               "//tr[contains(., '3newWH')]//a[contains(@class, 'edit') and contains(@class, 'actionButton')]",
                               Options(uniqueSelector=True))

        self.html.switchFrame("iframe")
        self.html.fillInput('Raktár neve', '33newWH')
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()

        self.stockAssert.assertWarehouseExist('33newWH')

        self.deleteWarehouse("33newWH")

    def testDelete(self):
        self.createWarehouse("4newWH")
        self.html.clickElement('4newWH', 'td[@class="sorting_1"]', Options(following='a'))
        self.html.clickElement("Igen", waitSeconds=2)

        self.stockAssert.assertWarehouseNotExist('4newWH')


if __name__ == "__main__":
    unittest.main()
