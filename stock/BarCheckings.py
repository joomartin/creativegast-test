from selenium.webdriver.common.keys import Keys
from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as td


class BarCheckings(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.stockseed.createWarehouse(td.WareHouse['Name'])
        self.stockseed.createRawMaterialWithOpening(td.RawMaterial['Name'], td.RawMaterial['GrosPrice'], td.RawMaterial['Quantity'], td.WareHouse['Name'])
        self.menu.openStocks()
        self.stockseed.createWarehouse('Araktár', module=True)
        self.stockseed.createRawMaterialWithOpening('Abszint', '1000', '10', 'Araktár', module=True)

        self.html.clickElement('Standellenőrzések', 'a')

    @classmethod
    def tearDownClass(self):
        #self.stockseed.deleteRawMaterial(td.RawMaterial['Name'])
        #self.stockseed.deleteWarehouse(td.WareHouse['Name'])
        #super().tearDownClass()
        pass

        self.stockseed.deleteRawMaterial('Abszint', module=True)
        self.stockseed.deleteWarehouse('Araktár', tab=True)
        super().tearDownClass()

    def deleteChecking(self):
        self.html.clickTableElement('barchecking', 'id', td.WareHouse['Name'], 'a', 'Törlés', 'Standellenőrzések')
        self.html.clickElement('Igen')
        self.html.refresh()

    def testCreate(self):
        self.html.clickElement('Új standellenőrzés', 'a')
        self.html.switchFrame('iframe')

        self.html.clickElement(td.WareHouse['Name'], 'label', Options(following='label'))
        self.html.clickElement('Indít', waitSeconds=3)
        qty = int(self.html.getElement(td.RawMaterial['Name'], 'td', Options(following='td[3]//input')).get_attribute('value'))
        modqty= qty - 5
        self.html.getElement(td.RawMaterial['Name'], 'td', Options(following='td[3]//input')).clear()
        self.html.getElement(td.RawMaterial['Name'], 'td', Options(following='td[3]//input')).send_keys(str(modqty))
        self.html.clickElement(td.RawMaterial['Name'], 'td', Options(following='button'))

        self.html.clickElement('Lezárás', 'a')
        self.html.refresh()

        self.html.clickTableElement('barchecking', 'id', td.WareHouse['Name'], 'a', 'Megtekintés', 'Standellenőrzések')

        self.html.switchFrame('iframe')

        summMiss = self.html.getTxtFromTable(3, 4)
        self.assertEqual(summMiss, '-5')

        matMiss = self.html.getTxtFromTable(3, 4)
        self.assertEqual(matMiss, '-5')

        self.html.clickElement('Mégsem')
        self.html.switchFrame()

        self.stockAssert.assertStock(td.RawMaterial['Name'], td.WareHouse['Name'], str(modqty))
        self.html.clickElement('Standellenőrzések', 'a')

        self.deleteChecking()

        self.stockAssert.assertStock(td.RawMaterial['Name'], td.WareHouse['Name'], str(qty))

