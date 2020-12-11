from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from shared.TestData import TestData as td
from seeders.ReceivingSeed import ReceivingSeed
from core.Options import Options
from shared.BaseTestCase import BaseTestCase

class Receiving(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)
        self.stockseed.createWarehouse(td.WareHouse['Name'], module=True)
        self.stockseed.createRawMaterialWithOpening(td.RawMaterial['Name'], td.RawMaterial['GrosPrice'], td.RawMaterial['Quantity'], td.WareHouse['Name'], module=True)
        self.receivingseed.createPartner(td.Partner['Name'],td.Partner['Id'], module=True)




    @classmethod
    def tearDownClass(self):
        self.stockseed.deleteRawMaterial(td.RawMaterial['Name'], module=True)
        self.stockseed.deleteWarehouse(td.WareHouse['Name'], module=True)
        self.receivingseed.deleteParter(td.Partner['Name'], module=True)
        super().tearDownClass()

    def createReceiving(self, billName,):
        self.menu.openReceiving()
        self.html.clickElement('Új bevételezés', 'a', waitSeconds=2)
        self.html.clickElement('Új')
        self.html.switchFrame('iframe')

        self.html.fillInput('Számla azonosító', billName)
        self.html.clickDropdown('Fizetési mód', 'Készpénz')
        self.html.clickDropdown('Beszállító', td.Partner['Name'])
        self.html.fillAutocomplete('Nyersanyag neve', 'input', td.RawMaterial['Name'], td.RawMaterial['Name'], 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '100', 'data-title')
        self.html.clickElement('Válassz...')
        self.html.clickElement(td.WareHouse['Name'], 'label')

        self.html.clickElement('Hozzáad')
        self.html.wait(2)
        self.html.clickElement('Rögzít')

        self.html.switchFrame()

    def testCreate(self):
        name= 'testBill'
        self.createReceiving(name)
        self.html.wait(2)
        self.receivingAssert.assertReceivingExists(td.Partner['Name'])
        self.html.clickElement('Törlés', 'span')
        self.html.clickElement('Igen')


    def testDetails(self):
        name = 'testBill'
        self.createReceiving(name)
        self.html.wait(2)
        self.receivingAssert.assertReceivingExists(td.Partner['Name'])
        self.html.clickElement('Részletek', 'span')
        self.html.switchFrame('iframe')
        self.receivingAssert.assertReceivingDetails(td.RawMaterial['Name'], '100')

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        self.html.clickElement('Törlés', 'span')
        self.html.clickElement('Igen')


