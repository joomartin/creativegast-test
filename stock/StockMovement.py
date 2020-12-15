from selenium.webdriver.common.keys import Keys
from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data


class StockMovement(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createWarehouse(data.WareHouses['Tartalékraktár']['Name'])
        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['GrosPrice'], data.RawMaterial['Bundas_kenyer']['Quantity'], data.WareHouses['Szeszraktár']['Name'], module=True)

        self.html.clickElement('Raktármozgás', 'a')

    @classmethod
    def tearDownClass(self):

        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)
        self.stockseed.deleteWarehouse(data.WareHouses['Tartalékraktár']['Name'])
        super().tearDownClass()


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
        self.html.fillInput('Mennyiség', data.WareHouses['Szeszraktár']['MoveQuantity'], 'data-title')
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()

    def deleteMovement(self, warehouse):
        self.html.clickTableElement('storagemove', 'id', warehouse, 'span', 'Töröl', 'Raktármozgás')
        self.html.clickElement('Igen')

    def testCreate(self):
        self.createNewMovement()
        self.deleteMovement(data.WareHouses['Szeszraktár']['Name'])

    def testView(self):
        self.createNewMovement()

        self.html.clickTableElement('storagemove', 'id', data.WareHouses['Szeszraktár']['Name'], 'span', 'Megtekintés', 'Raktármozgás')

        self.html.switchFrame('iframe')

        materialName = self.html.getTxtFromTable(2, 1)
        self.assertEqual(materialName, data.RawMaterial['Bundas_kenyer']['Name'])

        qty = self.html.getTxtFromTable(2, 2)
        self.assertEqual(qty, data.WareHouses['Szeszraktár']['MoveQuantity'])

        me = self.html.getTxtFromTable(2, 3)
        self.assertEqual(me, data.RawMaterial['Bundas_kenyer']['ME'])

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        qty = str(int(data.RawMaterial['Bundas_kenyer']['Quantity']) - int(data.WareHouses['Szeszraktár']['MoveQuantity']))
        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'], data.WareHouses['Tartalékraktár']['Name'], qty)
        self.html.clickElement('Raktármozgás', 'a')

        self.deleteMovement(data.WareHouses['Szeszraktár']['Name'])

        qty2 = str(int(data.RawMaterial['Bundas_kenyer']['Quantity']) - int(data.WareHouses['Szeszraktár']['MoveQuantity']) * 2)
        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'], data.WareHouses['Tartalékraktár']['Name'], qty2)