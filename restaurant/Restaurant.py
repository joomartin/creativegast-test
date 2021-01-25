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
        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['GrossPrice'],
                                         data.RawMaterial['Bundas_kenyer']['Quantity'], data.RawMaterial['Bundas_kenyer']['Warehouse'], me='db' ,module=True)

        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Alma']['Name'], data.RawMaterial['Alma']['GrosPrice'], data.RawMaterial['Alma']['Quantity'], data.RawMaterial['Alma']['Warehouse'], me='db')
        self.productseed.createCounter(data.Counter['TestCounter']['Name'], data.Counter['TestCounter']['Position'],
                                       module=True)
        self.productseed.createProductGroup(data.ProductGroup['Egyeb']['Name'], tab=True)
        self.html.wait(5)
        #self.productseed.createProductGroup(data.ProductGroup['Öntetek']['Name'])
        self.productseed.createProduct(data.Product['Babgulyás']['Name'], data.ProductGroup['Egyeb']['Name'],
                                       data.Product['Babgulyás']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.productseed.createProduct(data.Product['Palacsinta']['Name'], data.ProductGroup['Egyeb']['Name'],
                                       data.Product['Palacsinta']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.restaurantseed.createTable(data.Table['Normal']['Name'], module=True)
        self.menu.openRestaurant()


    @classmethod
    def tearDownClass(self):

        self.productseed.deleteProduct(data.Product['Babgulyás']['Name'], module=True)
        self.productseed.deleteProduct(data.Product['Palacsinta']['Name'], module=True)
        self.productseed.deleteCounter(data.Counter['TestCounter']['Name'], tab=True)
        self.productseed.deleteProductGroup(data.ProductGroup['Egyeb']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Alma']['Name'], module=True)
        self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)
        #self.productseed.deleteProductGroup(data.ProductGroup['Öntetek']['Name'], module=True)
        self.restaurantseed.deleteTable(data.Table['Normal']['Name'], module=True)
        super().tearDownClass()

    def setUp(self):
        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

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

    def testOrderStorno(self):

        self.addProductToList(data.Product['Babgulyás']['Name'], '1.00')
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

        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['Warehouse'], '6')

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        # johet a sztorno
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', data.Product['Babgulyás']['Name'], 'div', 'Sztornó')
        self.html.clickElement('Vendég visszamondta (raktárba visszatesz)', waitSeconds=2)
        self.assertFalse(self.html.getElement('Fizetés', 'button').is_displayed())

        self.html.wait(5)  # megkell varni h az ertesitesi ablak megjelenjen
        self.assertTrue(self.html.getElement(
            data.Product['Babgulyás']['Name'] + ' nevű termék a felszolgáló által sztornózva lett! ',
            'li').is_displayed())
        self.html.clickElement('Rendben', 'a')

        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                     data.RawMaterial['Bundas_kenyer']['Warehouse'], '8')

    def testOrderPayed(self):
        self.addProductToList(data.Product['Babgulyás']['Name'], '1.00')
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

        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                    data.RawMaterial['Bundas_kenyer']['Warehouse'], '8')

    def testUnion(self):
        inputName = data.Product['Babgulyás']['Name']

        self.addProductToList(inputName, '1.00')
        self.addProductToList(inputName, '1.00')
        #self.html.clickElement('aaaa', 'div') # ez a verzi nem az elso elemet jelolte ki
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', inputName)
        self.html.clickElement('Összevonás', waitSeconds=2)
        self.html.clickElement('Összevonás / Áthelyezés', waitSeconds=4)

        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        self.assertEqual(name.text, inputName)
        self.assertEqual(qty.text, '2.00')

        # törlés
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', 'Törlés')
        self.html.clickElement('Igen', waitSeconds=2)
        # itt azt csekkoljuk hogy a rendeles bekuldese gomb eltunt e
        self.assertFalse(self.html.getElement('Rendelés beküldése', 'button').is_displayed())

    def testUnfold(self):
        inputName = data.Product['Babgulyás']['Name']

        self.addProductToList(inputName, '1.00')
        self.addProductToList(inputName, '1.00')
        # self.html.clickElement('aaaa', 'div') # ez a verzi nem az elso elemet jelolte ki
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', inputName)
        self.html.clickElement('Összevonás', waitSeconds=2)
        self.html.clickElement('Összevonás / Áthelyezés', waitSeconds=2)

        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        self.assertEqual(name.text, inputName)
        self.assertEqual(qty.text, '2.00')

        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', inputName)
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

        self.assertEqual(name.text, inputName)
        self.assertEqual(qty.text, '1.00')
        self.assertEqual(name2.text, inputName)
        self.assertEqual(qty2.text, '1.00')

        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', 'Törlés')
        self.html.clickElement('Igen', waitSeconds=2)
        self.html.refresh()
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', 'Törlés')
        self.html.clickElement('Igen', waitSeconds=2)
        # itt azt csekkoljuk hogy a rendeles bekuldese gomb eltunt e
        self.assertFalse(self.html.getElement('Rendelés beküldése', 'button').is_displayed())

    def testUnionAll(self):
        inputName = data.Product['Babgulyás']['Name']
        inputName2 = data.Product['Palacsinta']['Name']

        self.addProductToList(inputName, '1.00')
        self.addProductToList(inputName, '1.00')
        self.addProductToList(inputName2, '1.00')
        self.addProductToList(inputName2, '1.00')

        self.html.clickElement('Minden összevonása', waitSeconds=4)

        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        name2 = self.html.getTxtFromListTable('3', '3', tableId='tasks-list products ui-sortable',
                                              options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        qty2 = self.html.getTxtFromListTable('3', '5', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))

        self.assertEqual(name.text, inputName2)
        self.assertEqual(qty.text, '2.00')
        self.assertEqual(name2.text, inputName)
        self.assertEqual(qty2.text, '2.00')

        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', 'Törlés')
        self.html.clickElement('Igen', waitSeconds=2)
        self.html.refresh()
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName2, 'div', 'Törlés')
        self.html.clickElement('Igen', waitSeconds=2)
        # itt azt csekkoljuk hogy a rendeles bekuldese gomb eltunt e
        self.assertFalse(self.html.getElement('Rendelés beküldése', 'button').is_displayed())

    def testMove(self):
        inputName = data.Product['Babgulyás']['Name']

        self.addProductToList(inputName, '1.00')
        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        self.assertEqual(name.text, inputName)
        self.assertEqual(qty.text, '1.00')

        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', inputName)
        self.html.clickElement('Áthelyez részasztalra')
        partTables = self.html.getElement('moveDialog', 'div', options=Options(htmlAttribute='id'))
        self.html.clickElement('2', 'a', options=Options(element=partTables), waitSeconds=4)

        tables = self.html.getElements('tasks-list products ui-sortable', 'table',
                                       options=Options(htmlAttribute='class'))

        #table = self.html.getElement('tasks-list products ui-sortable', 'table', options=Options(htmlAttribute='class'))
        nrows = tables[0].find_elements_by_tag_name('tr')
        print(len(nrows))
        self.assertEqual(len(nrows), 2)

        self.html.clickElement('2', 'a')
        #secondTable = self.html.getElement('tabs-3146', 'div', options=Options(htmlAttribute='id'))


        secondTable = tables[1]

        name2 = self.html.getTxtFromListTable2('2', '3',
                                             options=Options(element=secondTable))
        qty2 = self.html.getTxtFromListTable2('2', '5',
                                            options=Options(element=secondTable))
        self.assertEqual(name2.text, inputName)
        self.assertEqual(qty2.text, '1.00')

        self.html.clickElement('Törlés', 'a', options=Options(element=secondTable))
        #self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', 'Törlés')
        self.html.clickElement('Igen', waitSeconds=2)

        self.html.clickElement('1', 'a')

















