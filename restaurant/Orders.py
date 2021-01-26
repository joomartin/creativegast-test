from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options
import Restaurant


class Orders(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)
        self.restaurantseed.createTable(data.Table['Normal']['Name'], module=True)



    def setUp(self):
        self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Csirkemell']['Name'],
                                                    data.RawMaterial['Csirkemell']['GrosPrice'],
                                                    data.RawMaterial['Csirkemell']['Quantity'],
                                                    data.RawMaterial['Csirkemell']['Warehouse'], data.RawMaterial['Csirkemell']['ME'],
                                                    module=True)

        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Finomliszt']['Name'],
                                                    data.RawMaterial['Finomliszt']['GrosPrice'],
                                                    data.RawMaterial['Finomliszt']['Quantity'],
                                                    data.RawMaterial['Finomliszt']['Warehouse'], data.RawMaterial['Finomliszt']['ME'])

        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Almalé']['Name'],
                                                    data.RawMaterial['Almalé']['GrosPrice'],
                                                    data.RawMaterial['Almalé']['Quantity'],
                                                    data.RawMaterial['Almalé']['Warehouse'],
                                                    data.RawMaterial['Almalé']['ME'])

        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Hasábburgonya']['Name'],
                                                    data.RawMaterial['Hasábburgonya']['GrosPrice'],
                                                    data.RawMaterial['Hasábburgonya']['Quantity'],
                                                    data.RawMaterial['Hasábburgonya']['Warehouse'],
                                                    data.RawMaterial['Hasábburgonya']['ME'])

        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Sonka']['Name'],
                                                    data.RawMaterial['Sonka']['GrosPrice'],
                                                    data.RawMaterial['Sonka']['Quantity'],
                                                    data.RawMaterial['Sonka']['Warehouse'],
                                                    data.RawMaterial['Sonka']['ME'])

        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Paradicsomszósz']['Name'],
                                                    data.RawMaterial['Paradicsomszósz']['GrosPrice'],
                                                    data.RawMaterial['Paradicsomszósz']['Quantity'],
                                                    data.RawMaterial['Paradicsomszósz']['Warehouse'],
                                                    data.RawMaterial['Paradicsomszósz']['ME'])

        self.productseed.createCounter(data.Counter['TestCounter']['Name'], data.Counter['TestCounter']['Position'],
                                       module=True)
        #self.productseed.createProductGroup(data.ProductGroup['Egyeb']['Name'], tab=True)
        self.html.wait(5)

        self.productseed.createProduct(data.Product['Hasábburgonya']['Name'], 'Köretek',
                                       data.Product['Hasábburgonya']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Hasábburgonya']['Name'], data.Product['Hasábburgonya']['Quantity'],data.Product['Hasábburgonya']['NetPrice'], module=True)

        self.productseed.createProduct('Almalé', 'Kiszereléses',
                                       '99', data.Counter['TestCounter']['Name'], data.RawMaterial['Almalé']['Name'], '1', '2200', module=True)

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')


    @classmethod
    def tearDownClass(self):
        self.restaurantseed.deleteTable(data.Table['Normal']['Name'], module=True)
        super().tearDownClass()

    def tearDown(self):

        self.productseed.deleteProduct(data.Product['Hasábburgonya']['Name'], module=True)
        self.productseed.deleteProduct('Almalé')
        self.productseed.deleteCounter(data.Counter['TestCounter']['Name'], tab=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Csirkemell']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Finomliszt']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Almalé']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Hasábburgonya']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Sonka']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Paradicsomszósz']['Name'], module=True)
        self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)
        #self.productseed.deleteProductGroup(data.ProductGroup['Öntetek']['Name'], module=True)

    def createProductChose(self):
        self.html.clickElement('Új termék felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', 'Pult')
        self.html.switchFrame('iframe')

        self.html.clickElement('Ételek', 'a')
        self.html.clickElement('Rögzít')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', 'Roston csirkemell')

        self.html.clickElement('Ez a termék tartalmaz köretet', 'label', Options(following='i'))

        places = self.html.getElement('Eladási ár (Kötelező)', 'td')
        self.html.clickElement('Ár megadása', options=Options(element=places))
        self.html.fillInput('Nettó', '1800')
        self.html.wait(1)
        self.html.clickElement('taxPriceSave', 'a', options=Options(htmlAttribute='id'))
        self.html.wait(2)

        self.html.fillAutocomplete('componentName', 'input', 'Csirkemell', 'Csirkemell', 'li', Options(htmlAttribute='id'))
        self.html.fillInput('componentQty', '0.20', 'input', options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')


    def createProductFix(self):
        self.html.clickElement('Új termék felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', 'Pult')
        self.html.switchFrame('iframe')

        self.html.clickElement('Ételek', 'a')
        self.html.clickElement('Rögzít')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', 'Rántott csirkemell')

        self.html.clickElement('Ez a termék tartalmaz köretet', 'label', Options(following='i'))

        places = self.html.getElement('Eladási ár (Kötelező)', 'td')
        self.html.clickElement('Ár megadása', options=Options(element=places))
        self.html.fillInput('Nettó', '2200')
        self.html.wait(1)
        self.html.clickElement('taxPriceSave', 'a', options=Options(htmlAttribute='id'))
        self.html.wait(2)

        self.html.clickElement('Válasszon köretet')
        self.html.clickElement(data.Product['Hasábburgonya']['Name'], 'label')

        self.html.fillAutocomplete('componentName', 'input', 'Csirkemell', 'Csirkemell', 'li', Options(htmlAttribute='id'))
        self.html.fillInput('componentQty', '0.20', 'input', options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít')

    def addProductToList(self, productName, quantity):
        self.html.fillAutocomplete('Terméknév', 'input', productName[:-1], productName, 'li',
                                   Options(htmlAttribute='placeholder'))

        self.html.fillInput('Mennyiség', quantity, 'placeholder')
        self.html.clickElement('addProduct', 'a', options=Options(htmlAttribute='id'))
        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))

        print(qty.text)
        self.assertEqual(name.text, productName)
        self.assertEqual(qty.text, quantity)

    def testMultipleOrders(self):
        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()

        self.menu.openRestaurant()

        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.addProductToList('Rántott csirkemell', '1.00')
        self.html.clickElement('Ital', 'a')
        self.html.clickElement('Kiszereléses', 'a')
        self.html.wait(2)
        self.html.clickElement('Almalé', 'a')
        self.html.wait(2)
        self.html.switchFrame('iframe')
        gomb = self.html.getElement('3 dl', 'a')
        self.html.clickElement('3 dl', 'a')

        self.productseed.deleteProduct('Roston csirkemell', module=True)
        self.productseed.deleteProduct('Rántott csirkemell')