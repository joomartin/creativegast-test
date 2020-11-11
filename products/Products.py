from core.Options import Options
from shared.BaseTestCase import BaseTestCase

class Products(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openProducts()

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

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

        '''
        places = self.html.getElement('Eladási ár (Kötelező)', 'td')
        self.html.clickElement('Ár megadása', element=places)
        self.html.fillInput('Nettó', 100)
        self.html.clickElement('Rögzít')
        self.html.wait(2)
        '''

        self.html.fillAutocomplete('componentName', 'input', 'Captain', 'Captain Morgan 0.7 l', 'li', Options(htmlAttribute='id'))
        self.html.fillInput('componentQty', 2, 'input', options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

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
        editedCounter = ''
        editedCounterState = 11
        counter = '1asd'


        self.createProduct(name, group, 99, counter)

        self.html.clickTableElement('products', 'id', name, 'a', 'Szerkeszt', 'Termékek')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', 'Pizza')
        self.html.switchFrame('iframe')

        self.html.clickElement(group, 'a')
        self.html.clickElement(editedGroup, 'a')
        self.html.clickElement('Rögzít')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', editedName)
        self.html.fillInput('Kód', editedCode)

        #self.html.fillInput('Számláló neve', editedCounter)
        #self.html.fillInput('Számláló állás', editedCounterState)

        self.html.clickElement('Törlés')
        self.html.fillAutocomplete('componentName', 'input', 'Coca', 'Coca Cola 0.5 l', 'li',
                                   Options(htmlAttribute='id'))
        self.html.fillInput('componentQty', 1, 'input', options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')

        self.html.clickElement('Rögzít')
        self.html.search('', 'Termékek')

        self.productAssert.assertProductExist(editedName, 'Termékek')

        self.html.search(editedName, 'Termékek')
        self.html.clickTableElement('products', 'id', name, 'a', 'Részletek', 'Termékek')
        self.html.switchFrame('iframe')

        detailsTable = self.html.getElement('details', 'table', options=Options(htmlAttribute='class'))





    def testDetails(self):
        pass

    def testClone(self):
        pass


































