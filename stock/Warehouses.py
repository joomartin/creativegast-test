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


    def deleteWarehouse(self, warehouseName):
        self.html.refresh()

        self.html.wait(2)
        self.html.search(warehouseName, 'Raktárak')
        self.html.wait(2)
        currWindow = self.html.getElement('tabs-3', 'div', options=Options(htmlAttribute='id'))
        # itt azert adjuk at a currWindow-t, hogy az adott oldalon keressen a td-k kozott
        self.html.clickElement(warehouseName, 'td', Options(following='a'), element = currWindow)
        self.html.wait(2)
        self.html.clickElement('Igen')
        self.html.wait(2)
        self.html.search('', 'Raktárak')
        self.html.wait(2)


    def testCreateWarehouse(self):
        self.createWarehouse("kicsiraktar")
        self.stockAssert.assertWarehouseExist('kicsiraktar', 'Raktárak')
        self.html.search('', 'Raktárak')


        self.deleteWarehouse("kicsiraktar")

    #@unittest.skip
    def testCantCreate(self):
        self.createWarehouse("nagyraktar")
        self.html.clickElement('Új raktár felvitele', 'a')
        self.html.switchFrame("iframe")

        self.html.fillInput('Raktár neve', 'nagyraktar', )
        self.html.clickElement("Rögzít")

        self.stockAssert.assertDialogDisplayed()

        self.html.clearInput('Raktár neve')
        self.html.clickElement("Mégsem")

        self.deleteWarehouse("nagyraktar")

    #@unittest.skip
    def testEdit(self):
        self.createWarehouse("joraktar")
        self.html.clickElement(None,
                               "//tr[contains(., 'joraktar')]//a[contains(@class, 'edit') and contains(@class, 'actionButton')]",
                               Options(uniqueSelector=True))

        self.html.switchFrame("iframe")
        self.html.fillInput('Raktár neve', 'rosszraktar')
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()

        self.stockAssert.assertWarehouseExist('rosszraktar', 'Raktárak')
        self.html.search('', 'Raktárak')

        self.deleteWarehouse("rosszraktar")


    def testDelete(self):
        self.html.refresh()
        self.createWarehouse("csakraktar")
        self.html.search('csakraktar', 'Raktárak')
        currWindow = self.html.getElement('tabs-3', 'div', options=Options(htmlAttribute='id'))
        self.html.clickElement('csakraktar', 'td', Options(following='a'), element = currWindow)
        self.html.clickElement("Igen", waitSeconds=2)
        self.html.search('', 'Raktárak')

        self.stockAssert.assertWarehouseNotExist('csakraktar', 'Raktárak')
        self.html.search('', 'Raktárak')


if __name__ == "__main__":
    unittest.main()
