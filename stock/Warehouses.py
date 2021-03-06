from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data


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
        def wrapper():
            self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'])
            self.stockAssert.assertWarehouseExist(data.WareHouses['Szeszraktár']['Name'], 'Raktárak')
            self.html.search('', 'Raktárak')
            self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'])

        super(Test, self).runTest(wrapper, 'warehouse-testCreateWarehouse')

    #@unittest.skip
    def testCantCreate(self):
        def wrapper():
            self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'])
            self.html.clickElement('Új raktár felvitele', 'a')
            self.html.switchFrame('iframe')

            self.html.fillInput('Raktár neve', data.WareHouses['Szeszraktár']['Name'])
            self.html.clickElement('Rögzít')

            self.stockAssert.assertDialogDisplayed()

            self.html.clearInput('Raktár neve')
            self.html.clickElement('Mégsem')

            self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'])

        super(Test, self).runTest(wrapper, 'warehouse-testCantCreate')

    def testEdit(self):
        def wrapper():
            self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'])
            self.html.search(data.WareHouses['Szeszraktár']['Name'], 'Raktárak')
            self.html.clickElement(None,
                                   "//tr[contains(., " + data.WareHouses['Szeszraktár'][
                                       'Name'] + ")]//a[contains(@class, 'edit') and contains(@class, 'actionButton')]",
                                   Options(uniqueSelector=True))

            self.html.switchFrame('iframe')
            self.html.fillInput('Raktár neve', data.WareHouses['Tartalékraktár']['Name'])
            self.html.clickElement('Rögzít')

            self.html.switchFrame()
            self.html.refresh()

            self.stockAssert.assertWarehouseExist(data.WareHouses['Tartalékraktár']['Name'], 'Raktárak')
            self.html.search('', 'Raktárak')

            self.stockseed.deleteWarehouse(data.WareHouses['Tartalékraktár']['Name'])

        super(Test, self).runTest(wrapper, 'warehouse-testEdit')

    def testDelete(self):
        def wrapper():
            self.html.refresh()
            self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'])
            self.html.search(data.WareHouses['Szeszraktár']['Name'], 'Raktárak')
            currWindow = self.html.getElement('tabs-3', 'div', options=Options(htmlAttribute='id'))
            self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'td',
                                   Options(following='a', element=currWindow))
            self.html.clickElement("Igen", waitSeconds=2)
            self.html.search('', 'Raktárak')

            self.stockAssert.assertWarehouseNotExist(data.WareHouses['Szeszraktár']['Name'], 'Raktárak')
            self.html.search('', 'Raktárak')

        super(Test, self).runTest(wrapper, 'warehouse-testDelete')


