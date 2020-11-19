from selenium.webdriver.common.keys import Keys
from core.Options import Options
from shared.BaseTestCase import BaseTestCase


class StockMovement(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.stockseed.createWarehouse('Araktár')
        self.stockseed.createWarehouse('Braktár')
        self.stockseed.createRawMaterialWithOpening('Abszint', '1000', '10', 'Araktár')

        self.html.clickElement('Raktármozgás', 'a')

    @classmethod
    def tearDownClass(self):
        self.stockseed.deleteRawMaterial('Abszint')
        self.stockseed.deleteWarehouse('Araktár')
        self.stockseed.deleteWarehouse('Braktár')
        super().tearDownClass()

    def createNewMovement(self):
        self.html.wait()
        self.html.clickElement('Új raktármozgás', 'a', waitSeconds=2)
        self.html.clickElement('Új')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Forrás raktár','Araktár')
        self.html.wait()
        self.html.clickDropdown('Cél raktár', 'Braktár')

        self.html.fillAutocomplete('Nyersanyag', 'input', 'Abszint','Abszint', 'li', Options(htmlAttribute='data-title'))
        self.html.getElement('Maximum', 'input', Options(htmlAttribute='data-title')).click()
        self.html.wait()
        self.html.fillInput('Mennyiség', '5', 'data-title')
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()

    def deleteMovement(self, warehouse):
        self.html.clickTableElement('storagemove', 'id', warehouse, 'span', 'Töröl', 'Raktármozgás')
        self.html.clickElement('Igen')

    def testCreate(self):
        warehouse = 'Araktár'
        self.createNewMovement()
        self.deleteMovement(warehouse)

    def testView(self):
        warehouse = 'Araktár'
        self.createNewMovement()

        self.html.clickTableElement('storagemove', 'id', warehouse, 'span', 'Megtekintés', 'Raktármozgás')

        self.html.switchFrame('iframe')

        materialName = self.html.getTxtFromTable(2, 1)
        self.assertEqual(materialName, 'Abszint')

        qty = self.html.getTxtFromTable(2, 2)
        self.assertEqual(qty, '5',)

        me = self.html.getTxtFromTable(2, 3)
        self.assertEqual(me, 'liter')

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        self.stockAssert.assertStock('Abszint', 'Braktár', '5')
        self.html.clickElement('Raktármozgás', 'a')

        self.deleteMovement(warehouse)

        self.stockAssert.assertStock('Abszint', 'Braktár', '0')