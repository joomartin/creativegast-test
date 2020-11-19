from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from products.ProductGroups import ProductGroups as pg

class Products(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.pg = pg()
        self.tempGroup = 'ideiglenes'

        self.menu.openProducts()


        #self.createTempGroup(self, self.tempGroup)

    @classmethod
    def tearDownClass(self):
        #super().tearDownClass()
        #self.deleteTempGroup(self.tempGroup)
        pass

    '''
    @staticmethod
    def createProductGroup(html, groupName):
        html.clickElement('Új termékcsoport felvitele', 'a')

        html.switchFrame('iframe')

        html.fillInput('Termékcsoport neve', groupName)
        html.clickDropdown('Kategória', 'Étel')
        html.clickElement('Rögzít')
        html.switchFrame()
        html.wait(2)
    '''

    def createProduct(self, name, group, code, counter):
        self.html.clickElement('Új termék felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', 'Pult')
        self.html.switchFrame('iframe')

        self.html.clickElement(group, 'a')
        self.html.clickElement('Rögzít')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', name)
        self.html.fillInput('Kód', code)

        self.html.clickElement('p_counters', 'input', Options(htmlAttribute='id'), waitSeconds = 1)
        self.html.switchFrame('iframe')

        self.html.clickElement(counter, 'td')
        self.html.clickElement('Rögzít')
        self.html.switchFrame('iframe')


        places = self.html.getElement('Eladási ár (Kötelező)', 'td')
        self.html.clickElement('Ár megadása', element=places)
        self.html.fillInput('Nettó', 100)
        self.html.wait(2)
        self.html.clickElement('taxPriceSave', 'a', options=Options(htmlAttribute='id'))
        self.html.wait(5)


        self.html.fillAutocomplete('componentName', 'input', 'Captain', 'Captain Morgan 0.7 l', 'li', Options(htmlAttribute='id'))
        self.html.fillInput('componentQty', 2, 'input', options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')


    '''
    def createTempGroup(self, name):
        self.html.clickTab('Termékcsoportok')
        #self.pg.createProductGroup(name)
        self.createProductGroup(self.html, name)
        self.html.clickTab('Termékek')


    def deleteTempGroup(self, name):
        self.html.clickTab('Termékcsoportok')
        self.pg.deleteProductGroup(name)
        self.html.clickTab('Termékek')
    '''

    def deleteProduct(self, name):
        self.html.refresh()

        self.html.clickTableElement('products', 'id', name, 'a', 'Törlés', 'Termékek')
        self.html.clickElement('Igen', waitSeconds=1)
        self.html.search('', 'Termékek')


    def testCreate(self):
        name = 'bestProduct'

        self.createProduct(name, 'Szeszes italok', 99, '1asd')
        self.productAssert.assertProductExist(name, 'Termékek')
        self.deleteProduct(name)

    def testEdit(self):
        name = 'bestProduct'
        editedName = 'editedProduct'
        editedGroup = 'Üdítők'
        group = 'Szeszes italok'
        editedCode = '11'
        editedPlace = 'Pizza'
        editedCounter = ''
        editedCounterState = 11
        counter = '1asd'
        material = 'Captain Morgan 0.7 l'
        editedMaterial1 = 'Coca Cola 0.5 l'



        self.createProduct(name, group, 99, counter)

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

        #self.html.fillInput('Számláló neve', editedCounter)
        #self.html.fillInput('Számláló állás', editedCounterState)

        #self.html.clickElement('Törlés')
        self.html.fillAutocomplete('componentName', 'input', 'Coca', editedMaterial1, 'li',
                                   Options(htmlAttribute='id'))
        self.html.fillInput('componentQty', 1, 'input', options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

        self.productAssert.assertProductExist(editedName, 'Termékek')

        self.html.search(editedName, 'Termékek')
        self.html.clickTableElement('products', 'id', editedName, 'a', 'Részletek', 'Termékek')
        self.html.switchFrame('iframe')


        dName =  self.html.getElementTxtInTable(editedName, 'details', 'Termékek', attribute='class')
        dPlace = self.html.getElementTxtInTable(editedPlace, 'details', 'Termékek', attribute='class')
        dGroup = self.html.getElementTxtInTable(editedGroup, 'details', 'Termékek', attribute='class')
        dCode = self.html.getElementTxtInTable(editedCode, 'details', 'Termékek', attribute='class')
        self.assertEqual(dName, editedName)
        self.assertEqual(dPlace, editedPlace)
        self.assertEqual(dGroup, editedGroup)
        self.assertEqual(dCode, editedCode)

        cName =  self.html.getElementTxtInTable(editedMaterial1, 'components', 'Termékek', attribute='class')
        self.assertEqual(cName, editedMaterial1)
        cName2 = self.html.getElementTxtInTable(material, 'components', 'Termékek', attribute='class')
        self.assertEqual(cName2, material)

        self.html.switchFrame()
        self.html.clickElement('Close', 'a', Options(htmlAttribute='title'))
        self.html.search('', 'Termékek')



    def testDetails(self):
        pass


































