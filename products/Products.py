import unittest

from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data


class Products(BaseTestCase):
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
        self.stockseed.createRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'],
                                         data.RawMaterial['Bundas_kenyer']['ME'],
                                         data.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createRawMaterial(data.RawMaterial['Alma']['Name'], data.RawMaterial['Alma']['ME'],
                                         data.WareHouses['Szeszraktár']['Name'])
        '''
        for material in self.rawMaterials:
            self.stockseed.createRawMaterialWithOpening(data.RawMaterial[material]['Name'],
                                                        data.RawMaterial[material]['GrosPrice'],
                                                        data.RawMaterial[material]['Quantity'],
                                                        data.RawMaterial[material]['Warehouse'],
                                                        data.RawMaterial[material]['ME'],
                                                        module=True)
        '''
        self.productseed.createCounter(data.Counter['TestCounter']['Name'], data.Counter['TestCounter']['Position'],
                                       module=True)
        self.productseed.createProductGroup(data.ProductGroup['Egyeb']['Name'], tab=True)
        self.productseed.createProductGroup(data.ProductGroup['Öntetek']['Name'])
        self.menu.openProducts()

    def tearDown(self):
        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Alma']['Name'], module=True)
        self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)
        self.productseed.deleteCounter(data.Counter['TestCounter']['Name'], module=True)
        self.productseed.deleteProductGroup(data.ProductGroup['Egyeb']['Name'], module=True)
        self.productseed.deleteProductGroup(data.ProductGroup['Öntetek']['Name'], module=True)

    def testCreate(self):
        self.productseed.createProduct(data.Product['Babgulyás']['Name'], data.ProductGroup['Egyeb']['Name'],
                                       data.Product['Babgulyás']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Bundas_kenyer']['Name'])
        self.productAssert.assertProductExist(data.Product['Babgulyás']['Name'], 'Termékek')
        self.productseed.deleteProduct(data.Product['Babgulyás']['Name'])

    def testCreateConvenience(self):
        self.productseed.createProductConveniencies(data.Product['Babgulyás']['Name'],
                                                    data.ProductGroup['Egyeb']['Conveniences'],
                                                    data.Product['Babgulyás']['Code'], data.Counter['TestCounter']['Name'],
                                                    data.RawMaterial['Bundas_kenyer']['Name'])
        self.productAssert.assertProductExist(data.Product['Babgulyás']['Name'], 'Termékek')
        self.productseed.deleteProduct(data.Product['Babgulyás']['Name'])

    def testEdit(self):
        editedPlace = 'Pizza'
        editedName = 'Bableves'
        editedCode = '3131999'
        editedQuantity = '3'

        self.productseed.createProduct(data.Product['Babgulyás']['Name'], data.ProductGroup['Egyeb']['Name'], data.Product['Babgulyás']['Code'], data.Counter['TestCounter']['Name'], data.RawMaterial['Bundas_kenyer']['Name'])

        self.html.clickTableElement('products', 'id', data.Product['Babgulyás']['Name'], 'a', 'Szerkeszt', 'Termékek')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', editedPlace)
        self.html.switchFrame('iframe')

        self.html.clickElement(data.ProductGroup['Egyeb']['Name'], 'a')
        self.html.clickElement(data.ProductGroup['Öntetek']['Name'], 'a')
        self.html.clickElement('Rögzít')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', editedName)
        self.html.fillInput('Kód', editedCode)

        places = self.html.getElement('Eladási ár (Kötelező)', 'data')
        self.html.clickElement('edit actionButton fright editPriceBtn', 'a', options=Options(htmlAttribute='class', element=places))
        self.html.fillInput('Nettó', data.Product['Babgulyás']['NetPrice'])
        self.html.wait(2)
        self.html.clickElement('taxPriceSave', 'a', options=Options(htmlAttribute='id'))
        self.html.wait(2)

        #self.html.fillInput('Számláló neve', editedCounter)
        #self.html.fillInput('Számláló állás', editedCounterState)

        # self.html.clickElement('Törlés')
        self.html.fillAutocomplete('componentName', 'input', data.RawMaterial['Alma']['Name'], data.RawMaterial['Alma']['Name'], 'li',
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
        self.assertTrue(self.html.getRowExist(['Termékcsoport:', data.ProductGroup['Öntetek']['Name']]))
        self.assertTrue(self.html.getRowExist(['Kód:', editedCode]))
        # ez itt egy bug, lehala  teszt
        self.assertTrue(self.html.getTablePairsExist('Számláló(k):', data.Counter['TestCounter']['Name']))

        self.assertTrue(self.html.getRowExist(['Eladási ár', data.Product['Babgulyás']['NetPrice']]))

        # dPrice = self.html.getElementTxtInTable(editedPrice, 'onefourthTable', 'Termékek', attribute='class')
        # self.assertEqual(dPrice, editedPrice)

        # csekkoljuk, hogy a nyersanyagok megvannak e
        self.assertTrue(self.html.getRowExist([data.RawMaterial['Bundas_kenyer']['Name'], data.Product['Babgulyás']['Quantity'], data.RawMaterial['Bundas_kenyer']['ME'], '0']))
        self.assertTrue(self.html.getRowExist([data.RawMaterial['Alma']['Name'], editedQuantity, data.RawMaterial['Alma']['ME'], '0']))
        # cName =  self.html.getElementTxtInTable('Modified', 'components', 'Termékek', attribute='class')
        # self.assertEqual(cName, 'Modified')

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        self.html.search('', 'Termékek')

        self.productseed.deleteProduct(editedName)

    def testCreateProductAsRawMaterial(self):
        self.productseed.createProductAsRawMaterial(module=True)

        self.productAssert.assertProductExist('Kóla', 'Termékek')
        self.html.search('Kóla', 'Termékek')
        self.html.clickTableElement('products', 'id', 'Kóla', 'a', 'Részletek', 'Termékek')
        self.html.switchFrame('iframe')

        dName = self.html.getElementTxtInTable('Kóla', 'details', 'Termékek', attribute='class')
        self.assertEqual(dName, 'Kóla')
        self.assertTrue(self.html.getRowExist(['Termék neve:', 'Kóla']))
        self.assertTrue(self.html.getRowExist(['Nyomtatási részleg:', 'Pult']))
        self.assertTrue(self.html.getRowExist(['Termékcsoport:', 'Üdítők']))
        self.assertTrue(self.html.getRowExist(['Eladási ár', '300']))
        # csekkoljuk, hogy a nyersanyag megvan e
        self.assertTrue(self.html.getRowExist(['Kóla', '1', 'kg', '0']))

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        self.html.search('', 'Termékek')

        self.stockAssert.assertMaterialExist('Kóla', 'Raktárkészlet', module=True)

        self.productseed.deleteProduct('Kóla', module=True)
        self.stockseed.deleteRawMaterial('Kóla', module=True)

    @unittest.skip
    def testvalami(self):
        self.productseed.createProduct(data.Product['Hasábburgonya']['Name'], 'Köretek',
                                       data.Product['Hasábburgonya']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Hasábburgonya']['Name'],
                                       data.Product['Hasábburgonya']['Quantity'],
                                       data.Product['Hasábburgonya']['NetPrice'], module=True)




























