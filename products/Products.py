from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from products.ProductGroups import ProductGroups as pg

class Products(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        '''
        self.stockseed.createWarehouse('Araktár')
        self.stockseed.createRawMaterial('RawMaterial', 'liter', 'Araktár')
        self.stockseed.createRawMaterial('Modified', 'liter', 'Araktár')
        self.productseed.createCounter('ProductCounter', 0)
        self.productseed.createProductGroup('TestGroup')
        self.productseed.createProductGroup('ModGroup')
        '''
        self.menu.openProducts()




    @classmethod
    def tearDownClass(self):
        self.stockseed.deleteRawMaterial('RawMaterial')
        self.stockseed.deleteRawMaterial('Modified')
        self.stockseed.deleteWarehouse('Araktár')
        self.productseed.deleteCounter('ProductCounter')
        self.productseed.deleteProductGroup('TestGroup')
        self.productseed.deleteProductGroup('ModGroup')



    def testCreate(self):
        name = 'bestProduct'

        self.productseed.createProduct(name, 'TestGroup', 99, 'ProductCounter', 'RawMaterial')
        self.productAssert.assertProductExist(name, 'Termékek')
        self.productseed.deleteProduct(name)

    def testEdit(self):
        name = 'bestProduct'
        editedName = 'editedProduct'
        editedGroup = 'Üdítők'
        group = 'Szeszes italok'
        editedCode = '98'
        editedPlace = 'Pizza'
        editedCounter = ''
        editedCounterState = 98
        counter = 'ProductCounter'
        editedPrice = '200'


        '''
        self.productseed.createProduct(name, group, 99, 'ProductCounter', 'RawMaterial')

        self.html.clickTableElement('products', 'id', name, 'a', 'Szerkeszt', 'Termékek')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', editedPlace)
        self.html.switchFrame('iframe')

        self.html.clickElement(group, 'a')
        self.html.clickElement(editedGroup, 'a')
        self.html.clickElement('Rögzít')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', editedName)
        self.html.fillInput('Kód', editedCode)

        places = self.html.getElement('Eladási ár (Kötelező)', 'td')
        self.html.clickElement('edit actionButton fright editPriceBtn', 'a', options=Options(htmlAttribute='class'), element=places)
        self.html.fillInput('Nettó', editedPrice)
        self.html.wait(2)
        self.html.clickElement('taxPriceSave', 'a', options=Options(htmlAttribute='id'))
        self.html.wait(2)

        #self.html.fillInput('Számláló neve', editedCounter)
        #self.html.fillInput('Számláló állás', editedCounterState)

        # self.html.clickElement('Törlés')
        self.html.fillAutocomplete('componentName', 'input', 'Modified', 'Modified', 'li',
                                   Options(htmlAttribute='id'))
        self.html.fillInput('componentQty', 1, 'input', options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

        self.productAssert.assertProductExist(editedName, 'Termékek')
        '''
        self.html.search(editedName, 'Termékek')
        self.html.clickTableElement('products', 'id', editedName, 'a', 'Részletek', 'Termékek')
        self.html.switchFrame('iframe')


        dName =  self.html.getElementTxtInTable(editedName, 'details', 'Termékek', attribute='class')
        dPlace = self.html.getElementTxtInTable(editedPlace, 'details', 'Termékek', attribute='class')
        dGroup = self.html.getElementTxtInTable(editedGroup, 'details', 'Termékek', attribute='class')
        dCode = self.html.getElementTxtInTable(editedCode, 'details', 'Termékek', attribute='class')
        '''self.assertEqual(dName, editedName)
        self.assertEqual(dPlace, editedPlace)
        self.assertEqual(dGroup, editedGroup)
        self.assertEqual(dCode, editedCode)'''
        self.assertTrue(self.html.getTablePairsExist('Termék neve:', editedName))
        self.assertTrue(self.html.getTablePairsExist('Nyomtatási részleg:', editedPlace))
        self.assertTrue(self.html.getTablePairsExist('Termékcsoport:', editedGroup))
        self.assertTrue(self.html.getTablePairsExist('Kód:', editedCode))
        self.assertTrue(self.html.getTablePairsExist('Számláló(k):', counter))

        #dPrice = self.html.getElementTxtInTable(editedPrice, 'onefourthTable', 'Termékek', attribute='class')
        #self.assertEqual(dPrice, editedPrice)

        cName =  self.html.getElementTxtInTable('Modified', 'components', 'Termékek', attribute='class')
        self.assertEqual(cName, 'Modified')

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        self.html.search('', 'Termékek')

        self.productseed.deleteProduct('editedProduct')



    def testDetails(self):
        pass


































