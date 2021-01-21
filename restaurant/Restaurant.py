''' Na ez hosszu menet lesz...'''
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options


class Restaurant(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['ME'],
                                         data.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createRawMaterial(data.RawMaterial['Alma']['Name'], data.RawMaterial['Alma']['ME'],
                                         data.WareHouses['Szeszraktár']['Name'])
        self.productseed.createCounter(data.Counter['TestCounter']['Name'], data.Counter['TestCounter']['Position'],
                                       module=True)
        self.productseed.createProductGroup(data.ProductGroup['Egyeb']['Name'], tab=True)
        self.productseed.createProductGroup(data.ProductGroup['Öntetek']['Name'])
        self.productseed.createProduct(data.Product['Babgulyás']['Name'], data.ProductGroup['Egyeb']['Name'],
                                       data.Product['Babgulyás']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.restaurantseed.createTable(data.Table['Normal']['Name'], module=True)
        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

    @classmethod
    def tearDownClass(self):
        self.productseed.deleteProduct(data.Product['Babgulyás']['Name'], module=True)
        self.productseed.deleteCounter(data.Counter['TestCounter']['Name'], tab=True)
        self.productseed.deleteProductGroup(data.ProductGroup['Egyeb']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Alma']['Name'], module=True)
        self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)
        self.productseed.deleteProductGroup(data.ProductGroup['Öntetek']['Name'], module=True)
        self.restaurantseed.deleteTable(data.Table['Normal']['Name'], module=True)
        super().tearDownClass()


    def addProductToList(self, productName, quantity):
        self.html.fillAutocomplete('Terméknév', 'input', productName, productName, 'li',
                                   Options(htmlAttribute='placeholder'))

        self.html.fillInput('Mennyiség', quantity, 'placeholder')
        self.html.clickElement('addProduct', 'a', options=Options(htmlAttribute='id'))
        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        self.assertEqual(name.text, productName)
        self.assertEqual(qty.text, quantity+'.00')

    def testOrderStorno(self):

        self.addProductToList(data.Product['Babgulyás']['Name'], '1')
        self.html.refresh()
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        storno = self.html.getTxtFromListTable('2', '8', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        self.assertEqual(name.text, data.Product['Babgulyás']['Name'])
        self.assertEqual(qty.text, '1.00')
        self.assertEqual(storno.text, 'Sztornó')
        print(storno)

        # johet a sztorno
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', data.Product['Babgulyás']['Name'], 'div', 'Sztornó')
        self.html.clickElement('Vendég visszamondta (raktárba visszatesz)', waitSeconds=2)
        self.assertFalse(self.html.getElement('Fizetés', 'button').is_displayed())

    def testOrderPayed(self):
        self.addProductToList(data.Product['Babgulyás']['Name'], '1')
        self.html.refresh()
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        storno = self.html.getTxtFromListTable('2', '8', tableId='tasks-list products ui-sortable',
                                               options=Options(htmlAttribute='class'))
        self.assertEqual(name.text, data.Product['Babgulyás']['Name'])
        self.assertEqual(qty.text, '1.00')
        self.assertEqual(storno.text, 'Sztornó')

        self.html.clickElement('Fizetés')

        self.html.clickElement('Kitölt')

        self.html.clickElement('payDialogButton', 'button', Options(htmlAttribute='id'))
        self.html.refresh()

        #self.html.clickElement('A müveletet elvégeztem')

    '''
    def testUnion(self):
        self.addProductToList()
        self.addProductToList()
        #self.html.clickElement('aaaa', 'div') # ez a verzi nem az elso elemet jelolte ki
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', 'aaaa', 'div', 'aaaa')
        self.html.clickElement('Összevonás', waitSeconds=2)
        self.html.clickElement('Összevonás / Áthelyezés', waitSeconds=2)

        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        self.assertEqual(name.text, 'aaaa')
        self.assertEqual(qty.text, '2.00')

        # törlés
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', 'aaaa', 'div', 'Törlés')
        self.html.clickElement('Igen', waitSeconds=2)
        # itt azt csekkoljuk hogy a rendeles bekuldese gomb eltunt e
        self.assertFalse(self.html.getElement('Rendelés beküldése', 'button').is_displayed())


    def testUnfold(self):
        self.addProductToList()
        self.addProductToList()
        # self.html.clickElement('aaaa', 'div') # ez a verzi nem az elso elemet jelolte ki
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', 'aaaa', 'div', 'aaaa')
        self.html.clickElement('Összevonás', waitSeconds=2)
        self.html.clickElement('Összevonás / Áthelyezés', waitSeconds=2)

        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        self.assertEqual(name.text, 'aaaa')
        self.assertEqual(qty.text, '2.00')

        self.html.clickTableElement('tasks-list products ui-sortable', 'class', 'aaaa', 'div', 'aaaa')
        self.html.clickElement('Bontás', waitSeconds=2)
        self.html.clickElement('Bontás / Áthelyezés', waitSeconds=4)

        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        name2 = self.html.getTxtFromListTable('3', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        qty2 = self.html.getTxtFromListTable('3', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))

        self.assertEqual(name.text, 'aaaa')
        self.assertEqual(qty.text, '1.00')
        self.assertEqual(name2.text, 'aaaa')
        self.assertEqual(qty2.text, '1.00')

        self.html.clickTableElement('tasks-list products ui-sortable', 'class', 'aaaa', 'div', 'Törlés')
        self.html.clickElement('Igen', waitSeconds=2)
        self.html.refresh()
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', 'aaaa', 'div', 'Törlés')
        self.html.clickElement('Igen', waitSeconds=2)
        # itt azt csekkoljuk hogy a rendeles bekuldese gomb eltunt e
        self.assertFalse(self.html.getElement('Rendelés beküldése', 'button').is_displayed())
        '''