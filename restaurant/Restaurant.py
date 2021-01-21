''' Na ez hosszu menet lesz...'''
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as td
from core.Options import Options


class Restaurant(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)
        '''
        self.stockseed.createWarehouse(td.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createRawMaterial(td.RawMaterial['Bundas_kenyer']['Name'], td.RawMaterial['Bundas_kenyer']['ME'],
                                         td.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createRawMaterial(td.RawMaterial['Alma']['Name'], td.RawMaterial['Alma']['ME'],
                                         td.WareHouses['Szeszraktár']['Name'])
        self.productseed.createCounter(td.Counter['TestCounter']['Name'], td.Counter['TestCounter']['Position'],
                                       module=True)
        self.productseed.createProductGroup(td.ProductGroup['Egyeb']['Name'], tab=True)
        self.productseed.createProductGroup(td.ProductGroup['Öntetek']['Name'])
        self.productseed.createProduct(td.Product['Babgulyás']['Name'], td.ProductGroup['Egyeb']['Name'],
                                       td.Product['Babgulyás']['Code'], td.Counter['TestCounter']['Name'],
                                       td.RawMaterial['Bundas_kenyer']['Name'])
        '''
        self.menu.openRestaurant()
        self.html.clickElement('PULT', tag='i')

    @classmethod
    def tearDownClass(self):
        '''
        self.stockseed.deleteRawMaterial(td.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.stockseed.deleteRawMaterial(td.RawMaterial['Alma']['Name'], module=True)
        self.stockseed.deleteWarehouse(td.WareHouses['Szeszraktár']['Name'], tab=True)
        self.productseed.deleteCounter(td.Counter['TestCounter']['Name'], module=True)
        self.productseed.deleteProduct(td.Product['Babgulyás']['Name'])
        self.productseed.deleteProductGroup(td.ProductGroup['Egyeb']['Name'], module=True)
        self.productseed.deleteProductGroup(td.ProductGroup['Öntetek']['Name'], module=True)
        super().tearDownClass()
        '''
        pass

    def addProductToList(self):
        self.html.fillAutocomplete('Terméknév', 'input', 'aaa', 'aaaa', 'li',
                                   Options(htmlAttribute='placeholder'))

        self.html.fillInput('Mennyiség', '1', 'placeholder')
        self.html.clickElement('addProduct', 'a', options=Options(htmlAttribute='id'))
        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        self.assertEqual(name.text, 'aaaa')
        self.assertEqual(qty.text, '1.00')

    def testOrderSending(self):

        self.addProductToList()
        self.html.refresh()
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)
        self.html.clickElement('PULT', tag='i')

        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        storno = self.html.getTxtFromListTable('2', '8', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        self.assertEqual(name.text, 'aaaa')
        self.assertEqual(qty.text, '1.00')
        self.assertEqual(storno.text, 'Sztornó')
        print(storno)

        # johet a sztorno
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', 'aaaa', 'div', 'Sztornó')
        self.html.clickElement('Vendég visszamondta (raktárba visszatesz)', waitSeconds=2)
        self.assertFalse(self.html.getElement('Fizetés', 'button').is_displayed())


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
