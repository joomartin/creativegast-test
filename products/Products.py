from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as td


class Products(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def setUp(self):
        self.stockseed.createWarehouse(td.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createRawMaterial(td.RawMaterial['Bundas_kenyer']['Name'], td.RawMaterial['Bundas_kenyer']['ME'],
                                         td.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createRawMaterial(td.RawMaterial['Alma']['Name'], td.RawMaterial['Alma']['ME'],
                                         td.WareHouses['Szeszraktár']['Name'])
        self.productseed.createCounter(td.Counter['TestCounter']['Name'], td.Counter['TestCounter']['Position'],
                                       module=True)
        self.productseed.createProductGroup(td.ProductGroup['Egyeb']['Name'], tab=True)
        self.productseed.createProductGroup(td.ProductGroup['Öntetek']['Name'])
        self.menu.openProducts()

    def tearDown(self):
        self.stockseed.deleteRawMaterial(td.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.stockseed.deleteRawMaterial(td.RawMaterial['Alma']['Name'], module=True)
        self.stockseed.deleteWarehouse(td.WareHouses['Szeszraktár']['Name'], tab=True)
        self.productseed.deleteCounter(td.Counter['TestCounter']['Name'], module=True)
        self.productseed.deleteProductGroup(td.ProductGroup['Egyeb']['Name'], module=True)
        self.productseed.deleteProductGroup(td.ProductGroup['Öntetek']['Name'], module=True)

    def testCreate(self):
        self.productseed.createProduct(td.Product['Babgulyás']['Name'], td.ProductGroup['Egyeb']['Name'], td.Product['Babgulyás']['Code'], td.Counter['TestCounter']['Name'], td.RawMaterial['Bundas_kenyer']['Name'])
        self.productAssert.assertProductExist(td.Product['Babgulyás']['Name'], 'Termékek')
        self.productseed.deleteProduct(td.Product['Babgulyás']['Name'])

    def testCreateConvenience(self):
        self.productseed.createProductConveniencies(td.Product['Babgulyás']['Name'], td.ProductGroup['Egyeb']['Conveniences'], td.Product['Babgulyás']['Code'], td.Counter['TestCounter']['Name'], td.RawMaterial['Bundas_kenyer']['Name'])
        self.productAssert.assertProductExist(td.Product['Babgulyás']['Name'], 'Termékek')
        self.productseed.deleteProduct(td.Product['Babgulyás']['Name'])

    def testEdit(self):
        editedPlace = 'Pizza'
        editedName = 'Bableves'
        editedCode = '3131999'
        editedQuantity = '3'

        self.productseed.createProduct(td.Product['Babgulyás']['Name'], td.ProductGroup['Egyeb']['Name'], td.Product['Babgulyás']['Code'], td.Counter['TestCounter']['Name'], td.RawMaterial['Bundas_kenyer']['Name'])

        self.html.clickTableElement('products', 'id', td.Product['Babgulyás']['Name'], 'a', 'Szerkeszt', 'Termékek')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', editedPlace)
        self.html.switchFrame('iframe')

        self.html.clickElement(td.ProductGroup['Egyeb']['Name'], 'a')
        self.html.clickElement(td.ProductGroup['Öntetek']['Name'], 'a')
        self.html.clickElement('Rögzít')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', editedName)
        self.html.fillInput('Kód', editedCode)

        places = self.html.getElement('Eladási ár (Kötelező)', 'td')
        self.html.clickElement('edit actionButton fright editPriceBtn', 'a', options=Options(htmlAttribute='class', element=places))
        self.html.fillInput('Nettó', td.Product['Babgulyás']['NetPrice'])
        self.html.wait(2)
        self.html.clickElement('taxPriceSave', 'a', options=Options(htmlAttribute='id'))
        self.html.wait(2)

        #self.html.fillInput('Számláló neve', editedCounter)
        #self.html.fillInput('Számláló állás', editedCounterState)

        # self.html.clickElement('Törlés')
        self.html.fillAutocomplete('componentName', 'input', td.RawMaterial['Alma']['Name'], td.RawMaterial['Alma']['Name'], 'li',
                                   Options(htmlAttribute='id'))
        self.html.fillInput('componentQty', editedQuantity, 'input', options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

        self.productAssert.assertProductExist(editedName, 'Termékek')

        self.html.search(editedName, 'Termékek')
        self.html.clickTableElement('products', 'id', editedName, 'a', 'Részletek', 'Termékek')
        self.html.switchFrame('iframe')

        dName = self.html.getElementTxtInTable(editedName, 'details', 'Termékek', attribute='class')
        self.assertEqual(dName, editedName)
        self.assertTrue(self.html.getRowExist(['Termék neve:', editedName]))
        self.assertTrue(self.html.getRowExist(['Nyomtatási részleg:', editedPlace]))
        self.assertTrue(self.html.getRowExist(['Termékcsoport:', td.ProductGroup['Öntetek']['Name']]))
        self.assertTrue(self.html.getRowExist(['Kód:', editedCode]))
        # ez itt egy bug, lehala  teszt
        self.assertTrue(self.html.getTablePairsExist('Számláló(k):', td.Counter['TestCounter']['Name']))

        self.assertTrue(self.html.getRowExist(['Eladási ár', td.Product['Babgulyás']['NetPrice']]))

        # dPrice = self.html.getElementTxtInTable(editedPrice, 'onefourthTable', 'Termékek', attribute='class')
        # self.assertEqual(dPrice, editedPrice)

        # csekkoljuk, hogy a nyersanyagok megvannak e
        self.assertTrue(self.html.getRowExist([td.RawMaterial['Bundas_kenyer']['Name'], td.Product['Babgulyás']['Quantity'], td.RawMaterial['Bundas_kenyer']['ME'], '0']))
        self.assertTrue(self.html.getRowExist([td.RawMaterial['Alma']['Name'], editedQuantity, td.RawMaterial['Alma']['ME'], '0']))
        # cName =  self.html.getElementTxtInTable('Modified', 'components', 'Termékek', attribute='class')
        # self.assertEqual(cName, 'Modified')

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        self.html.search('', 'Termékek')

        self.productseed.deleteProduct(editedName)



































