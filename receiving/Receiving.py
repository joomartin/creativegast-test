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
        self.stockseed.createWarehouse(td.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createRawMaterialWithOpening(td.RawMaterial['Bundas_kenyer']['Name'], td.RawMaterial['Bundas_kenyer']['GrossPrice'], td.RawMaterial['Bundas_kenyer']['Quantity'], td.WareHouses['Szeszraktár']['Name'], module=True)
        self.receivingseed.createPartner(td.Partner['Szallito']['Name'],td.Partner['Szallito']['Id'], module=True)




    @classmethod
    def tearDownClass(self):
        self.stockseed.deleteRawMaterial(td.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.stockseed.deleteWarehouse(td.WareHouses['Szeszraktár']['Name'], module=True)
        self.receivingseed.deleteParter(td.Partner['Szallito']['Name'], module=True)
        super().tearDownClass()

    def createReceiving(self, billName,):
        self.menu.openReceiving()
        self.html.clickElement('Új bevételezés', 'a', waitSeconds=2)
        # self.html.clickElement('Új')
        self.html.switchFrame('iframe')

        self.html.fillInput('Számla azonosító', billName)
        self.html.clickDropdown('Fizetési mód', 'Készpénz')
        self.html.clickDropdown('Beszállító', td.Partner['Szallito']['Name'])
        self.html.fillAutocomplete('Nyersanyag neve', 'input', td.RawMaterial['Bundas_kenyer']['Name'], td.RawMaterial['Bundas_kenyer']['Name'], 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '100', 'data-title')
        self.html.clickElement('Válassz...')
        self.html.clickElement(td.WareHouses['Szeszraktár']['Name'], 'label')

        self.html.clickElement('Hozzáad')
        self.html.wait(2)
        self.html.clickElement('Rögzít')

        self.html.switchFrame()

    def testCreate(self):
        name= 'testBill'
        self.createReceiving(name)
        self.html.wait(2)
        self.receivingAssert.assertReceivingExists(td.Partner['Szallito']['Name'])
        self.stockAssert.assertStock(td.RawMaterial['Bundas_kenyer']['Name'],td.WareHouses['Szeszraktár']['Name'],'110')
        self.menu.openReceiving()
        self.html.clickElement('Keresés')
        self.html.wait(2)
        self.html.clickElement('Törlés', 'span')
        self.html.clickElement('Igen')


    def testDetails(self):
        name = 'testBill'
        self.createReceiving(name)
        self.html.wait(2)
        self.receivingAssert.assertReceivingExists(td.Partner['Szallito']['Name'])
        self.html.clickElement('Részletek', 'span')
        self.html.switchFrame('iframe')
        self.receivingAssert.assertReceivingDetails(td.RawMaterial['Bundas_kenyer']['Name'], '100')

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        self.stockAssert.assertStock(td.RawMaterial['Bundas_kenyer']['Name'], td.WareHouses['Szeszraktár']['Name'], '110')
        self.menu.openReceiving()
        self.html.clickElement('Keresés')
        self.html.wait(2)
        self.html.clickElement('Törlés', 'span')
        self.html.clickElement('Igen')


