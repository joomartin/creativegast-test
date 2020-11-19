from selenium.webdriver.common.keys import Keys
from core.Options import Options
from shared.BaseTestCase import BaseTestCase


class BarCheckings(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.stockseed.createWarehouse('Araktár')
        self.stockseed.createRawMaterialWithOpening('Abszint', '1000', '10', 'Araktár')
        self.menu.openStocks()
        self.html.clickElement('Standellenőrzések', 'a')

    @classmethod
    def tearDownClass(self):
        self.stockseed.deleteRawMaterial('Abszint')
        self.stockseed.deleteWarehouse('Araktár')
        super().tearDownClass()


    def deleteChecking(self):
        warehouse = 'Araktár'
        self.html.clickTableElement('barchecking', 'id', warehouse, 'a', 'Törlés', 'Standellenőrzések')
        self.html.clickElement('Igen')
        self.html.refresh()

    def testCreate(self):
        warehouse = 'Araktár'
        self.html.clickElement('Új standellenőrzés', 'a')
        self.html.switchFrame('iframe')

        self.html.clickElement(warehouse, 'label', Options(following='label'))
        self.html.clickElement('Indít', waitSeconds=3)
        qty = int(self.html.getElement('Abszint', 'td', Options(following='td[3]//input')).get_attribute('value'))
        modqty= qty - 5
        self.html.getElement('Abszint', 'td', Options(following='td[3]//input')).clear()
        self.html.getElement('Abszint', 'td', Options(following='td[3]//input')).send_keys(str(modqty))
        self.html.clickElement('Abszint', 'td', Options(following='button'))

        self.html.clickElement('Lezárás', 'a')
        self.html.refresh()

        self.html.clickTableElement('barchecking', 'id', warehouse, 'a', 'Megtekintés', 'Standellenőrzések')

        self.html.switchFrame('iframe')

        summMiss = self.html.getTxtFromTable(3, 4)
        self.assertEqual(summMiss, '-5')

        matMiss = self.html.getTxtFromTable(3, 4)
        self.assertEqual(matMiss, '-5')

        self.html.clickElement('Mégsem')
        self.html.switchFrame()

        self.stockAssert.assertStock('Abszint', 'Araktár', str(modqty))
        self.html.clickElement('Standellenőrzések', 'a')

        self.deleteChecking()

        self.stockAssert.assertStock('Abszint', 'Araktár', str(qty))

