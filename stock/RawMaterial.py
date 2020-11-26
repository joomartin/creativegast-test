from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as td


class RawMaterial(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.stockseed.createWarehouse(td.WareHouse['Name'], module=True)


    @classmethod
    def tearDownClass(self):
        self.stockseed.deleteWarehouse(td.WareHouse['Name'], tab=True)
        super().tearDownClass()
        pass


    def testCreate(self):
        testName = 'Abszint'
        self.stockseed.createRawMaterial(td.RawMaterial['Name'], td.RawMaterial['ME'], td.WareHouse['Name'])
        self.stockseed.deleteRawMaterial(td.RawMaterial['Name'])


    def testUpdate(self):
        testName = 'Abszint'
        ME = 'liter'
        price = '1 010.00'

        self.stockseed.createRawMaterial(td.RawMaterial['Name'], td.RawMaterial['ME'], td.WareHouse['Name'])
        #self.html.search(testName, 'Raktárkészlet')
        #self.html.clickElement(testName, 'td', Options(following='a'))
        self.html.clickTableDropdown(td.RawMaterial['Name'], 'Szerkeszt', 'Raktárkészlet')
        self.html.switchFrame('iframe')

        self.html.fillInput('Bruttó beszerzési egységár', td.RawMaterial['ModifiedGrossPrice'])
        self.html.clickElement('Rögzít')
        self.html.switchFrame()
        self.html.refresh()

        self.html.search(td.RawMaterial['Name'], 'Raktárkészlet')
        new = self.html.getTxtFromTable('1', '6', 'components')
        self.assertEqual(td.RawMaterial['ModifiedGrossPrice'], new)

        self.stockseed.deleteRawMaterial(td.RawMaterial['Name'])

    def testOpening(self):
        testName = 'Abszint'

        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyersanyag neve', td.RawMaterial['Name'])
        self.html.fillInput('Bruttó beszerzési egységár', td.RawMaterial['GrosPrice'])
        self.html.clickDropdown('ME', td.RawMaterial['ME'])
        self.html.fillInput('Nyitó mennyiség', td.RawMaterial['Quantity'])
        self.html.clickDropdown('Raktár', td.WareHouse['Name'])
        self.html.clickElement('Rögzít')
        self.html.switchFrame()
        self.html.refresh()

        self.html.search(td.RawMaterial['Name'], 'Raktárkészlet')
        quantity = self.html.getTxtFromTable(1, 3, 'components')
        #self.assertEqual('10.00', quantity)
        self.assertEqual(td.RawMaterial['FloatQuantity'], quantity)

        netPrice = self.html.getTxtFromTable(1, 5, 'components')
        self.assertEqual(td.RawMaterial['NetPrice'], '787.40')

        nettValue = self.html.getTxtFromTable(1, 7, 'components')
        self.assertEqual(td.RawMaterial['NetValue'], '7 874.02')

        self.html.clickTableDropdown(td.RawMaterial['Name'], 'Raktárak', 'Raktárkészlet')
        self.html.switchFrame('iframe')

        whause = self.html.getTxtFromTable(2, 2)
        self.assertEqual(whause, td.WareHouse['Name'])

        grossPrice = self.html.getTxtFromTable(2, 3)
        self.assertEqual(grossPrice, td.RawMaterial['GrosPrice'])

        qty = self.html.getTxtFromTable(2, 4)
        self.assertEqual(qty, td.RawMaterial['Quantity'])

        whValue = self.html.getTxtFromTable(2, 5)
        self.assertEqual(whValue, td.RawMaterial['WhValue'])

        # self.html.pressKey('iframe', 'body', Keys.ESCAPE, Options(htmlAttribute='class'))
        # self.html.switchFrame()
        # self.menu.openStocks()
        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))

        self.stockAssert.assertStock(td.RawMaterial['Name'], td.WareHouse['Name'], td.RawMaterial['Quantity'])

        self.stockseed.deleteRawMaterial(td.RawMaterial['Name'])

        self.stockAssert.assertDeletedMaterial(td.RawMaterial['Name'], td.WareHouse['Name'])

    def testDuplicate(self):
        testName = 'Abszint'

        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyersanyag neve', td.RawMaterial['Name'])
        self.html.clickDropdown('ME', td.RawMaterial['ME'])
        self.html.clickDropdown('Raktár', td.WareHouse['Name'])
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

        self.html.refresh()
        self.html.search(td.RawMaterial['Name'], 'Raktárkészlet')
        self.stockAssert.assertMaterialExist(td.RawMaterial['Name'], 'Raktárkészlet')

        self.html.clickElement('Új nyersanyag felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyersanyag neve', td.RawMaterial['Name'])
        self.html.clickDropdown('ME', td.RawMaterial['ME'])
        self.html.clickDropdown('Raktár', td.WareHouse['Name'])
        self.html.clickElement('Rögzít')

        self.stockAssert.assertDialogDisplayed()

        self.html.clickElement('Mégse')
        self.html.clickElement('Igen')
        self.html.switchFrame()

        self.stockseed.deleteRawMaterial(td.RawMaterial['Name'])

    def testWastingRawMaterial(self):
        testName = 'Abszint'
        ME = 'liter'

        self.stockseed.createRawMaterial(td.RawMaterial['Name'], td.RawMaterial['ME'], td.WareHouse['Name'])
        # self.html.search(testName, 'Raktárkészlet')
        # self.html.clickElement(testName, 'td',  Options(following='a'))
        self.html.clickTableDropdown(td.RawMaterial['Name'], 'Szerkeszt', 'Raktárkészlet')
        self.html.switchFrame('iframe')

        self.html.fillInput('Nyitó mennyiség', td.RawMaterial['Quantity'])
        self.html.clickDropdown('Raktár', td.WareHouse['Name'])
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

        self.html.clickTableDropdown(td.RawMaterial['Name'], 'Selejt', 'Raktárkészlet')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Raktár', td.WareHouse['Name'])
        self.html.fillInput('Mennyiség', td.RawMaterial['Waste'])
        self.html.clickElement('Üveg összetört')
        self.html.switchFrame()
        self.html.refresh()

        self.html.search(td.RawMaterial['Name'], 'Raktárkészlet')
        qty = self.html.getTxtFromTable(1, 3, 'components')
        self.assertEqual(qty, td.RawMaterial['FloatWaste'])

        self.stockAssert.assertStock(td.RawMaterial['Name'], td.WareHouse['Name'], td.RawMaterial['Waste'])

        self.stockseed.deleteRawMaterial(td.RawMaterial['Name'])

        self.stockAssert.assertDeletedMaterial(td.RawMaterial['Name'], 'Pult',)

    def testOpeningButton(self):
        ME = 'liter'
        qty = '100'
        self.stockseed.createRawMaterial(td.RawMaterial['Name'], td.RawMaterial['ME'], td.WareHouse['Name'])

        self.html.search(td.RawMaterial['Name'], 'Raktárkészlet')
        self.html.clickElement(td.RawMaterial['Name'], 'td', Options(following='a'))
        self.html.clickElement('Nyitókészlet', 'a')

        self.html.switchFrame('iframe')
        input = self.html.getElement(td.RawMaterial['Name'], 'td', Options(following='input'))
        input.send_keys(td.RawMaterial['Quantity2'])

        self.html.clickDropdown(td.RawMaterial['Name'], td.WareHouse['Name'], 'td')
        self.html.clickElement('Rögzít', 'span', waitSeconds=2)

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))


        self.html.refresh()
        self.stockAssert.assertStock(td.RawMaterial['Name'], td.WareHouse['Name'], td.RawMaterial['Quantity2'])

        self.stockseed.deleteRawMaterial(td.RawMaterial['Name'])








