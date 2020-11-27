from selenium.webdriver.common.keys import Keys
from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as td


class StockMovement(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.stockseed.createWarehouse(td.WareHouse['Name'], module=True)
        self.stockseed.createWarehouse(td.WareHouse2['Name'])
        self.stockseed.createRawMaterialWithOpening(td.RawMaterial['Name'], td.RawMaterial['GrosPrice'], td.RawMaterial['Quantity'], td.WareHouse['Name'], module=True)

        self.html.clickElement('Raktármozgás', 'a')

    @classmethod
    def tearDownClass(self):
        self.stockseed.deleteRawMaterial(td.RawMaterial['Name'], module=True)
        self.stockseed.deleteWarehouse(td.WareHouse['Name'], tab=True)
        self.stockseed.deleteWarehouse(td.WareHouse2['Name'])
        super().tearDownClass()

    def createNewMovement(self):
        self.html.wait()
        self.html.clickElement('Új raktármozgás', 'a', waitSeconds=2)
        self.html.clickElement('Új')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Forrás raktár',td.WareHouse['Name'])
        self.html.wait()
        self.html.clickDropdown('Cél raktár', td.WareHouse2['Name'])

        self.html.fillAutocomplete('Nyersanyag', 'input', td.RawMaterial['Name'], td.RawMaterial['Name'], 'li', Options(htmlAttribute='data-title'))
        self.html.getElement('Maximum', 'input', Options(htmlAttribute='data-title')).click()
        self.html.wait()
        self.html.fillInput('Mennyiség', td.WareHouse['MoveQuantity'], 'data-title')
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()

    def deleteMovement(self, warehouse):
        self.html.clickTableElement('storagemove', 'id', warehouse, 'span', 'Töröl', 'Raktármozgás')
        self.html.clickElement('Igen')

    def testCreate(self):
        self.createNewMovement()
        self.deleteMovement(td.WareHouse['Name'])

    def testView(self):
        self.createNewMovement()

        self.html.clickTableElement('storagemove', 'id', td.WareHouse['Name'], 'span', 'Megtekintés', 'Raktármozgás')

        self.html.switchFrame('iframe')

        materialName = self.html.getTxtFromTable(2, 1)
        self.assertEqual(materialName, td.RawMaterial['Name'])

        qty = self.html.getTxtFromTable(2, 2)
        self.assertEqual(qty, td.WareHouse['MoveQuantity'])

        me = self.html.getTxtFromTable(2, 3)
        self.assertEqual(me, td.RawMaterial['ME'])

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        qty = str(int(td.RawMaterial['Quantity']) - int(td.WareHouse['MoveQuantity']))
        self.stockAssert.assertStock(td.RawMaterial['Name'], td.WareHouse2['Name'], qty)
        self.html.clickElement('Raktármozgás', 'a')

        self.deleteMovement(td.WareHouse['Name'])

        qty2 = str(int(td.RawMaterial['Quantity']) - int(td.WareHouse['MoveQuantity'])*2)
        self.stockAssert.assertStock(td.RawMaterial['Name'], td.WareHouse2['Name'], qty2)