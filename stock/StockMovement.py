from selenium.webdriver.common.keys import Keys
from core.Options import Options
from shared.BaseTestCase import BaseTestCase


class StockMovement(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openStocks()
        self.html.clickElement('Raktármozgás', 'a')

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def createNewMovement(self):
        self.html.wait()
        self.html.clickElement('Új raktármozgás', 'a', waitSeconds=2)
        self.html.clickElement('Új')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Forrás raktár','Pult')
        self.html.wait()
        self.html.clickDropdown('Cél raktár', 'Dugipia raktár')

        self.html.fillAutocomplete('Nyersanyag', 'input', 'Coca','Coca Cola 025l', 'li', Options(htmlAttribute='data-title'))
        self.html.getElement('Maximum', 'input', Options(htmlAttribute='data-title')).click()
        self.html.wait()
        self.html.fillInput('Mennyiség', '11', 'data-title')
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

        self.html.switchFrame()
        self.html.refresh()

    def deleteMovement(self, warehouse):
        self.html.clickTableElement('storagemove', 'id', warehouse, 'span', 'Töröl', 'Raktármozgás')
        self.html.clickElement('Igen')

    def testCreate(self):
        warehouse = 'Pult'
        self.createNewMovement()
        self.deleteMovement(warehouse)

    def testView(self):
        warehouse = 'Pult'
        self.createNewMovement()

        self.html.clickTableElement('storagemove', 'id', warehouse, 'span', 'Megtekintés', 'Raktármozgás')

        self.html.switchFrame('iframe')

        materialName = self.html.getTxtFromTable(2, 1)
        self.assertEqual(materialName, 'Coca Cola 025l')

        qty = self.html.getTxtFromTable(2, 2)
        self.assertEqual(qty, '11',)

        me = self.html.getTxtFromTable(2, 3)
        self.assertEqual(me, 'db')

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        self.stockAssert.assertStock('Coca Cola 025l', 'Dugipia raktár', '11')
        self.html.clickElement('Raktármozgás', 'a')

        self.deleteMovement(warehouse)

        self.stockAssert.assertStock('Coca Cola 025l', 'Dugipia raktár', '0')