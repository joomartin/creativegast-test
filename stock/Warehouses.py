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



    def testCreateWarehouse(self):
        self.data.createWarehouse("kicsiraktar")
        self.stockAssert.assertWarehouseExist('kicsiraktar', 'Raktárak')
        self.html.search('', 'Raktárak')


        self.data.deleteWarehouse("kicsiraktar")

    #@unittest.skip
    def testCantCreate(self):
        self.data.createWarehouse("nagyraktar")
        self.html.clickElement('Új raktár felvitele', 'a')
        self.html.switchFrame("iframe")

        self.html.fillInput('Raktár neve', 'nagyraktar', )
        self.html.clickElement("Rögzít")

        self.stockAssert.assertDialogDisplayed()

        self.html.clearInput('Raktár neve')
        self.html.clickElement("Mégsem")

        self.data.deleteWarehouse("nagyraktar")

    #@unittest.skip
    def testEdit(self):
        self.data.createWarehouse("joraktar")
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

        self.data.deleteWarehouse("rosszraktar")


    def testDelete(self):
        self.html.refresh()
        self.data.createWarehouse("csakraktar")
        self.html.search('csakraktar', 'Raktárak')
        currWindow = self.html.getElement('tabs-3', 'div', options=Options(htmlAttribute='id'))
        self.html.clickElement('csakraktar', 'td', Options(following='a'), element = currWindow)
        self.html.clickElement("Igen", waitSeconds=2)
        self.html.search('', 'Raktárak')

        self.stockAssert.assertWarehouseNotExist('csakraktar', 'Raktárak')
        self.html.search('', 'Raktárak')


if __name__ == "__main__":
    unittest.main()
