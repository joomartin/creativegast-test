import unittest

from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data


class RawMaterial(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def setUp(self):
        self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'], module=True)

    def tearDown(self):
        self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)

    def testCreate(self):
        self.stockseed.createRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'],
                                         data.RawMaterial['Bundas_kenyer']['ME'],
                                         data.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'])

    def testUpdate(self):

        self.stockseed.createRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['ME'], data.WareHouses['Szeszraktár']['Name'], module=True)
        self.html.clickTableDropdown(data.RawMaterial['Bundas_kenyer']['Name'], 'Szerkeszt', 'Raktárkészlet')
        self.html.switchFrame('iframe')

        self.html.fillInput('Bruttó beszerzési egységár', data.RawMaterial['Bundas_kenyer']['GrossPrice'])
        self.html.clickElement('Rögzít')
        self.html.switchFrame()
        self.html.refresh()

        self.html.search(data.RawMaterial['Bundas_kenyer']['Name'], 'Raktárkészlet')
        new = self.html.getTxtFromTable('1', '6', 'components')
        self.assertEqual(data.RawMaterial['Bundas_kenyer']['GrossPrice'], new)

        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'])

    @unittest.skip
    def testOpening(self):
        calcNetPrice = self.html.extendedRound(int(float(data.RawMaterial['Bundas_kenyer']['GrossPrice'].replace(' ', ''))) / 1.27, 2)
        calcNetValue = self.html.extendedRound((int(float(data.RawMaterial['Bundas_kenyer']['GrossPrice'].replace(' ', ''))) / 1.27) * int(float(data.RawMaterial['Bundas_kenyer']['Quantity'].replace(' ', ''))), 2)
        calcWhValue = int(float(data.RawMaterial['Bundas_kenyer']['GrossPrice'].replace(' ', ''))) * int(float(data.RawMaterial['Bundas_kenyer']['Quantity'].replace(' ', '')))
        self.menu.openStocks()

        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyersanyag neve', data.RawMaterial['Bundas_kenyer']['Name'])
        self.html.fillInput('Bruttó beszerzési egységár', data.RawMaterial['Bundas_kenyer']['GrossPrice'])
        self.html.clickDropdown('ME', data.RawMaterial['Bundas_kenyer']['ME'])
        self.html.fillInput('Nyitó mennyiség', data.RawMaterial['Bundas_kenyer']['Quantity'])
        self.html.clickDropdown('Raktár', data.WareHouses['Szeszraktár']['Name'])
        self.html.clickElement('Rögzít')
        self.html.switchFrame()
        self.html.refresh()

        self.html.search(data.RawMaterial['Bundas_kenyer']['Name'], 'Raktárkészlet')
        quantity = self.html.getTxtFromTable(1, 3, 'components')
        #self.assertEqual('10.00', quantity)
        self.assertEqual(data.RawMaterial['Bundas_kenyer']['Quantity'], quantity.replace(' ', ''))

        netPrice = self.html.getTxtFromTable(1, 5, 'components')
        self.assertEqual(calcNetPrice, netPrice.replace(' ', ''))

        nettValue = self.html.getTxtFromTable(1, 7, 'components')
        self.assertEqual(calcNetValue, nettValue.replace(' ', ''))

        self.html.clickTableDropdown(data.RawMaterial['Bundas_kenyer']['Name'], 'Raktárak', 'Raktárkészlet')
        self.html.switchFrame('iframe')

        whause = self.html.getTxtFromTable(2, 2)
        self.assertEqual(whause, data.WareHouses['Szeszraktár']['Name'])

        grossPrice = self.html.getTxtFromTable(2, 3)
        self.assertEqual(grossPrice, str(int(float(data.RawMaterial['Bundas_kenyer']['GrossPrice'].replace(' ', '')))))

        qty = self.html.getTxtFromTable(2, 4)
        self.assertEqual(qty, str(int(float(data.RawMaterial['Bundas_kenyer']['Quantity'].replace(' ', '')))))

        whValue = self.html.getTxtFromTable(2, 5)
        self.assertEqual(whValue, str(calcWhValue))

        # self.html.pressKey('iframe', 'body', Keys.ESCAPE, Options(htmlAttribute='class'))
        # self.html.switchFrame()
        # self.menu.openStocks()
        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))

        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                     data.WareHouses['Szeszraktár']['Name'],
                                     str(int(float(data.RawMaterial['Bundas_kenyer']['Quantity']))))

        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'])

        self.stockAssert.assertDeletedMaterial(data.RawMaterial['Bundas_kenyer']['Name'], data.WareHouses['Szeszraktár']['Name'])

    @unittest.skip
    def testDuplicate(self):

        self.menu.openStocks()
        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyersanyag neve', data.RawMaterial['Bundas_kenyer']['Name'])
        self.html.clickDropdown('ME', data.RawMaterial['Bundas_kenyer']['ME'])
        self.html.clickDropdown('Raktár', data.WareHouses['Szeszraktár']['Name'])
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

        self.html.refresh()
        self.html.search(data.RawMaterial['Bundas_kenyer']['Name'], 'Raktárkészlet')
        self.stockAssert.assertMaterialExist(data.RawMaterial['Bundas_kenyer']['Name'], 'Raktárkészlet')

        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyersanyag neve', data.RawMaterial['Bundas_kenyer']['Name'])
        self.html.clickDropdown('ME', data.RawMaterial['Bundas_kenyer']['ME'])
        self.html.clickDropdown('Raktár', data.WareHouses['Szeszraktár']['Name'])
        self.html.clickElement('Rögzít')

        self.stockAssert.assertDialogDisplayed()

        self.html.clickElement('Mégse')
        self.html.clickElement('Igen')
        self.html.switchFrame()

        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'])

    def testWastingRawMaterial(self):
        def wrapper():
            self.stockseed.createRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['ME'], data.WareHouses['Szeszraktár']['Name'], module=True)
            # self.html.search(testName, 'Raktárkészlet')
            # self.html.clickElement(testName, 'td',  Options(following='a'))
            self.html.clickTableDropdown(data.RawMaterial['Bundas_kenyer']['Name'], 'Szerkeszt', 'Raktárkészlet')
            self.html.switchFrame('iframe')

            self.html.fillInput('Nyitó mennyiség', data.RawMaterial['Bundas_kenyer']['Quantity'])
            self.html.clickDropdown('Raktár', data.WareHouses['Szeszraktár']['Name'])
            self.html.clickElement('Rögzít')
            self.html.switchFrame()

            self.html.clickTableDropdown(data.RawMaterial['Bundas_kenyer']['Name'], 'Selejt', 'Raktárkészlet')
            self.html.wait(2)
            self.html.switchFrame('iframe')

            self.html.clickDropdown('Raktár', data.WareHouses['Szeszraktár']['Name'])
            self.html.fillInput('Mennyiség', data.RawMaterial['Bundas_kenyer']['Waste'])
            self.html.clickElement('Üveg összetört')
            self.html.switchFrame()
            self.html.refresh()

            self.html.search(data.RawMaterial['Bundas_kenyer']['Name'], 'Raktárkészlet')
            qty = self.html.getTxtFromTable(1, 3, 'components')
            self.assertEqual(qty, data.RawMaterial['Bundas_kenyer']['Waste'])

            self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                         data.WareHouses['Szeszraktár']['Name'],
                                         str(int(float(data.RawMaterial['Bundas_kenyer']['Waste']))))

            self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'])

            self.stockAssert.assertDeletedMaterial(data.RawMaterial['Bundas_kenyer']['Name'], data.WareHouses['Szeszraktár']['Name'])

        super(RawMaterial, self).runTest(wrapper, 'rawMaterial-testWastingRawMaterial')

    @unittest.skip
    def testOpeningButton(self):
        self.stockseed.createRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['ME'], data.WareHouses['Szeszraktár']['Name'], module=True)

        self.html.search(data.RawMaterial['Bundas_kenyer']['Name'], 'Raktárkészlet')
        self.html.clickElement(data.RawMaterial['Bundas_kenyer']['Name'], 'td', Options(following='a'))
        self.html.clickElement('Nyitókészlet', 'a')

        self.html.switchFrame('iframe')
        input = self.html.getElement(data.RawMaterial['Bundas_kenyer']['Name'], 'td', Options(following='input'))
        input.send_keys(data.RawMaterial['Bundas_kenyer']['Quantity2'])

        self.html.clickDropdown(data.RawMaterial['Bundas_kenyer']['Name'], data.WareHouses['Szeszraktár']['Name'], 'td')
        self.html.clickElement('Rögzít', 'span', waitSeconds=2)

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))


        self.html.refresh()
        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                     data.WareHouses['Szeszraktár']['Name'],
                                     str(int(float(data.RawMaterial['Bundas_kenyer']['Quantity2']))))

        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'])

    def testCreateRawMaterialWithOpening(self):
        def wrapper():
            rawMaterials = ['Csirkemell', 'Finomliszt', 'Almalé', 'Hasábburgonya', 'Sonka', 'Paradicsomszósz']

            for material in rawMaterials:
                self.stockseed.createRawMaterialWithOpening(data.RawMaterial[material]['Name'],
                                                            data.RawMaterial[material]['GrosPrice'],
                                                            data.RawMaterial[material]['Quantity'],
                                                            data.RawMaterial[material]['Warehouse'],
                                                            data.RawMaterial[material]['ME'],
                                                            module=True)

            for material in rawMaterials:
                self.stockAssert.assertMaterialExist(data.RawMaterial[material]['Name'], 'Raktárkészlet')

            for material in rawMaterials:
                self.stockseed.deleteRawMaterial(data.RawMaterial[material]['Name'], module=True)

        super(RawMaterial, self).runTest(wrapper, 'rawMaterial-testCreateRawMaterialWithOpening')
