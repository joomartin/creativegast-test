import unittest

from shared.TestData import TestData as data
from core.Options import Options
from shared.BaseTestCase import BaseTestCase


class Receiving(BaseTestCase):
    rawMaterials = ['Csirkemell', 'Finomliszt', 'Almalé', 'Hasábburgonya', 'Sonka', 'Paradicsomszósz']

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def setUp(self):
        self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Bundas_kenyer']['Name'],
                                                    data.RawMaterial['Bundas_kenyer']['GrossPrice'],
                                                    data.RawMaterial['Bundas_kenyer']['Quantity'],
                                                    data.WareHouses['Szeszraktár']['Name'], module=True)
        for material in self.rawMaterials:
            self.stockseed.createRawMaterialWithOpening(data.RawMaterial[material]['Name'],
                                                        data.RawMaterial[material]['GrosPrice'],
                                                        data.RawMaterial[material]['Quantity'],
                                                        data.RawMaterial[material]['Warehouse'],
                                                        data.RawMaterial[material]['ME'],
                                                        module=True)
        self.receivingseed.createPartner(data.Partner['Szallito']['Name'], data.Partner['Szallito']['Id'], module=True)

    def tearDown(self):
        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        for material in self.rawMaterials:
            self.stockseed.deleteRawMaterial(data.RawMaterial[material]['Name'], module=True)

        self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], module=True)
        self.receivingseed.deleteParter(data.Partner['Szallito']['Name'], module=True)

    def createReceiving(self, billName):
        self.menu.openReceiving()
        self.html.clickElement('Új bevételezés', 'a', waitSeconds=2)
        try:
            self.html.clickElement('Új')
        except Exception:
            pass
        self.html.switchFrame('iframe')

        self.html.fillInput('Számla azonosító', billName)
        self.html.clickDropdown('Fizetési mód', 'Készpénz')
        self.html.clickDropdown('Beszállító', data.Partner['Szallito']['Name'])
        self.html.fillAutocomplete('Nyersanyag neve', 'input', data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['Name'], 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '100', 'data-title')
        self.html.clickElement('Válassz...')
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')

        self.html.clickElement('Hozzáad')
        self.html.wait(2)
        self.html.clickElement('Rögzít')

        self.html.switchFrame()

    @unittest.skip
    def testCreate(self):
        name= 'testBill'
        self.createReceiving(name)
        self.html.wait(2)
        self.receivingAssert.assertReceivingExists(data.Partner['Szallito']['Name'])
        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],data.WareHouses['Szeszraktár']['Name'],'110')
        self.menu.openReceiving()
        self.html.clickElement('Keresés')
        self.html.wait(2)
        self.html.clickElement('Törlés', 'span')
        self.html.clickElement('Igen')

    @unittest.skip
    def testDetails(self):
        name = 'testBill'
        self.createReceiving(name)
        self.html.wait(2)
        self.receivingAssert.assertReceivingExists(data.Partner['Szallito']['Name'])
        self.html.clickElement('Részletek', 'span')
        self.html.switchFrame('iframe')
        self.receivingAssert.assertReceivingDetails(data.RawMaterial['Bundas_kenyer']['Name'], '100')

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'], data.WareHouses['Szeszraktár']['Name'], '110')
        self.menu.openReceiving()
        self.html.clickElement('Keresés')
        self.html.wait(2)
        self.html.clickElement('Törlés', 'span')
        self.html.clickElement('Igen')

    # ez igy fos, at kell majd irni de mukodik
    def testReceiving(self):
        self.productseed.createProductAsRawMaterial(module=True)

        self.receivingseed.createReceiving()

        self.stockAssert.assertStock(data.RawMaterial['Csirkemell']['Name'], data.WareHouses['Szeszraktár']['Name'],
                                     '20')
        self.html.wait(2)

        self.stockAssert.assertStock(data.RawMaterial['Finomliszt']['Name'], data.WareHouses['Szeszraktár']['Name'],
                                     '20')
        self.html.wait(2)

        self.stockAssert.assertStock(data.RawMaterial['Almalé']['Name'], data.WareHouses['Szeszraktár']['Name'], '20')
        self.html.wait(2)

        self.stockAssert.assertStock(data.RawMaterial['Hasábburgonya']['Name'], data.WareHouses['Szeszraktár']['Name'],
                                     '20')
        self.html.wait(2)

        self.stockAssert.assertStock(data.RawMaterial['Sonka']['Name'], data.WareHouses['Szeszraktár']['Name'], '20')
        self.html.wait(2)

        self.stockAssert.assertStock(data.RawMaterial['Paradicsomszósz']['Name'],
                                     data.WareHouses['Szeszraktár']['Name'], '20')
        self.html.wait(2)

        self.stockAssert.assertStock('Kóla', data.WareHouses['Szeszraktár']['Name'], '10')
        self.html.wait(2)

        self.productseed.deleteProduct('Kóla', module=True)
        self.stockseed.deleteRawMaterial('Kóla', module=True)
