from selenium.webdriver.common.keys import Keys
from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data


class StockMovement(BaseTestCase):
    moveQuantity = 5

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def setUp(self):
        self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createWarehouse(data.WareHouses['Tartalékraktár']['Name'])
        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Bundas_kenyer']['Name'],
                                                    data.RawMaterial['Bundas_kenyer']['GrossPrice'],
                                                    data.RawMaterial['Bundas_kenyer']['Quantity'],
                                                    data.WareHouses['Szeszraktár']['Name'], module=True)

        self.html.clickElement('Raktármozgás', 'a')

    def tearDown(self):
        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)
        self.stockseed.deleteWarehouse(data.WareHouses['Tartalékraktár']['Name'])

    def createNewMovement(self):
        self.html.wait()
        self.html.clickElement('Új raktármozgás', 'a', waitSeconds=2)
        self.html.clickElement('Új')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Forrás raktár', data.WareHouses['Szeszraktár']['Name'])
        self.html.wait()
        self.html.clickDropdown('Cél raktár', data.WareHouses['Tartalékraktár']['Name'])

        self.html.fillAutocomplete('Nyersanyag', 'input', data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['Name'], 'li', Options(htmlAttribute='data-title'))
        self.html.getElement('Maximum', 'input', Options(htmlAttribute='data-title')).click()
        self.html.wait()
        self.html.fillInput('Mennyiség', self.moveQuantity, 'data-title')
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()

    def deleteMovement(self, warehouse):
        self.html.clickTableElement('storagemove', 'id', warehouse, 'span', 'Töröl', 'Raktármozgás')
        self.html.clickElement('Igen')

    def testCreate(self):
        def wrapper():
            self.createNewMovement()
            self.deleteMovement(data.WareHouses['Szeszraktár']['Name'])

        super(StockMovement, self).runTest(wrapper, 'stockMovement-testCreate')

    def testView(self):
        def wrapper():
            self.createNewMovement()

            self.html.clickTableElement('storagemove', 'id', data.WareHouses['Szeszraktár']['Name'], 'span',
                                        'Megtekintés', 'Raktármozgás')

            self.html.switchFrame('iframe')

            materialName = self.html.getTxtFromTable(2, 1)
            self.assertEqual(materialName, data.RawMaterial['Bundas_kenyer']['Name'])

            qty = self.html.getTxtFromTable(2, 2)
            self.assertEqual(qty, str(self.moveQuantity))

            me = self.html.getTxtFromTable(2, 3)
            self.assertEqual(me, data.RawMaterial['Bundas_kenyer']['ME'])

            self.html.switchFrame()
            self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
            qty = str(int(float(data.RawMaterial['Bundas_kenyer']['Quantity'])) - self.moveQuantity)
            self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                         data.WareHouses['Tartalékraktár']['Name'], qty)
            self.html.clickElement('Raktármozgás', 'a')

            self.deleteMovement(data.WareHouses['Szeszraktár']['Name'])

            qty2 = str(int(float(data.RawMaterial['Bundas_kenyer']['Quantity'])) - self.moveQuantity * 2)
            self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                         data.WareHouses['Tartalékraktár']['Name'], qty2)

        super(StockMovement, self).runTest(wrapper, 'stockMovement-testView')
