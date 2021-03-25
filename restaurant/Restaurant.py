''' Na ez hosszu menet lesz...'''
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options


class Restaurant(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.restaurantseed.createTable(data.Table['Normal']['Name'], module=True)
        self.restaurantseed.createTable(data.Table['Courier']['Name'], module=True)

    def setUp(self):
        self.stockseed.createWarehouse(data.WareHouses['Szeszraktár']['Name'], module=True)
        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Bundas_kenyer']['Name'],
                                                    data.RawMaterial['Bundas_kenyer']['GrossPrice'],
                                                    data.RawMaterial['Bundas_kenyer']['Quantity'],
                                                    data.RawMaterial['Bundas_kenyer']['Warehouse'], me='db',
                                                    module=True)

        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Alma']['Name'],
                                                    data.RawMaterial['Alma']['GrosPrice'],
                                                    data.RawMaterial['Alma']['Quantity'],
                                                    data.RawMaterial['Alma']['Warehouse'], me='db')
        self.productseed.createCounter(data.Counter['TestCounter']['Name'], data.Counter['TestCounter']['Position'],
                                       module=True)
        self.productseed.createProductGroup(data.ProductGroup['Egyeb']['Name'], tab=True)
        self.html.wait(5)
        # self.productseed.createProductGroup(data.ProductGroup['Öntetek']['Name'])
        self.productseed.createProduct(data.Product['Babgulyás']['Name'], data.ProductGroup['Egyeb']['Name'],
                                       data.Product['Babgulyás']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.productseed.createProduct(data.Product['Palacsinta']['Name'], data.ProductGroup['Egyeb']['Name'],
                                       data.Product['Palacsinta']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Bundas_kenyer']['Name'], module=True)

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

    @classmethod
    def tearDownClass(self):
        self.restaurantseed.deleteTable(data.Table['Normal']['Name'], module=True)
        self.restaurantseed.deleteTable(data.Table['Courier']['Name'], module=True)
        super().tearDownClass()

    def tearDown(self):
        self.productseed.deleteProduct(data.Product['Babgulyás']['Name'], module=True)
        self.productseed.deleteProduct(data.Product['Palacsinta']['Name'], module=True)
        self.productseed.deleteCounter(data.Counter['TestCounter']['Name'], tab=True)
        self.productseed.deleteProductGroup(data.ProductGroup['Egyeb']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Alma']['Name'], module=True)
        self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)
        #self.productseed.deleteProductGroup(data.ProductGroup['Öntetek']['Name'], module=True)

    def addProductToList(self, productName, quantity):
        self.html.fillAutocomplete('Terméknév', 'input', productName[:-1], productName, 'li',
                                   Options(htmlAttribute='placeholder'))

        self.html.fillInput('Mennyiség', quantity, 'placeholder')
        self.html.clickElement('addProduct', 'a', options=Options(htmlAttribute='id'))
        name = self.html.getTxtFromListTable2('2', '3')
        qty = self.html.getTxtFromListTable2('2', '5')

        self.assertEqual(name.text, productName)
        self.assertEqual(qty.text, quantity)

    def testOrderPayed(self):
        self.addProductToList(data.Product['Babgulyás']['Name'], '1.00')
        self.html.refresh()
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        name = self.html.getTxtFromListTable2('2', '3')
        qty = self.html.getTxtFromListTable2('2', '5')
        storno = self.html.getTxtFromListTable2('2', '8')

        self.assertEqual(name.text, data.Product['Babgulyás']['Name'])
        self.assertEqual(qty.text, '1.00')
        self.assertEqual(storno.text, 'Sztornó')

        self.html.clickElement('Fizetés')
        self.html.clickElement('Kitölt')

        self.html.clickElement('payDialogButton', 'button', Options(htmlAttribute='id'))
        self.html.refresh()

        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                    data.RawMaterial['Bundas_kenyer']['Warehouse'], '8')

    def testOrderStorno(self):
        # mennyiseg ellenorzese
        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                     data.RawMaterial['Bundas_kenyer']['Warehouse'], '10')

        # vissza az etterembe
        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        self.addProductToList(data.Product['Babgulyás']['Name'], '1.00')
        self.html.refresh()
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        name = self.html.getTxtFromListTable2('2', '3')
        qty = self.html.getTxtFromListTable2('2', '5')
        storno = self.html.getTxtFromListTable2('2', '8')

        self.assertEqual(name.text, data.Product['Babgulyás']['Name'])
        self.assertEqual(qty.text, '1.00')
        self.assertEqual(storno.text, 'Sztornó')

        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['Warehouse'], '8')

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        # johet a sztorno
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', data.Product['Babgulyás']['Name'], 'div', 'Sztornó')
        self.html.clickElement('Vendég visszamondta (raktárba visszatesz)', waitSeconds=2)
        self.restaurantAssert.assertProductNotInList()
        self.restaurantAssert.assertStornoSucces(data.Product['Babgulyás']['Name'])

        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                     data.RawMaterial['Bundas_kenyer']['Warehouse'], '10')

    def testQualityStorno(self):
        # mennyiseg ellenorzese
        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                     data.RawMaterial['Bundas_kenyer']['Warehouse'], '10')
        # vissza az etterembe
        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        # rendeles bekuldese
        self.addProductToList(data.Product['Babgulyás']['Name'], '1.00')
        self.html.refresh()
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        name = self.html.getTxtFromListTable2('2', '3')
        qty = self.html.getTxtFromListTable2('2', '5')
        storno = self.html.getTxtFromListTable2('2', '8')

        # csekkolas
        self.assertEqual(name.text, data.Product['Babgulyás']['Name'])
        self.assertEqual(qty.text, '1.00')
        self.assertEqual(storno.text, 'Sztornó')

        # ez lehet itt nem kell, de nem baj ha van
        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['Warehouse'], '8')

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        # johet a sztorno
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', data.Product['Babgulyás']['Name'], 'div', 'Sztornó')
        self.html.clickElement('Minőségi kifogás', waitSeconds=1)
        self.html.fillInput('Minőségi kifogás indoka', 'teszt01 sztornó', 'textarea', options=Options(htmlAttribute='placeholder'))
        self.html.clickElement('Minőségi kifogás küldése', waitSeconds=2)

        self.restaurantAssert.assertProductNotInList()
        self.restaurantAssert.assertStornoSucces(data.Product['Babgulyás']['Name'])

        # mennyiseg ellenorzese
        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                     data.RawMaterial['Bundas_kenyer']['Warehouse'], '8')
        # selejt ellenorzese
        self.html.clickElement('Selejtezések', 'a')
        name = self.html.getElementInTable(data.RawMaterial['Bundas_kenyer']['Name'], 'component_waste', 'Selejtezések').is_displayed()
        excuse = self.html.getTxtFromTable('1', '5', 'component_waste')
        self.assertTrue(name)
        self.assertEqual(excuse, 'teszt01 sztornó')

    def testWrongorderStorno(self):
        # mennyiseg ellenorzese
        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                     data.RawMaterial['Bundas_kenyer']['Warehouse'], '10')
        # vissza az etterembe
        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        # rendeles bekuldese
        self.addProductToList(data.Product['Babgulyás']['Name'], '1.00')
        self.html.refresh()
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        name = self.html.getTxtFromListTable2('2', '3')
        qty = self.html.getTxtFromListTable2('2', '5')
        storno = self.html.getTxtFromListTable2('2', '8')

        self.assertEqual(name.text, data.Product['Babgulyás']['Name'])
        self.assertEqual(qty.text, '1.00')
        self.assertEqual(storno.text, 'Sztornó')

        # ez lehet itt nem kell, de nem baj ha van
        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'], data.RawMaterial['Bundas_kenyer']['Warehouse'], '8')

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        # johet a sztorno
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', data.Product['Babgulyás']['Name'], 'div', 'Sztornó')
        self.html.clickElement('Hibás rendelés (raktárba visszatesz)', waitSeconds=4)

        self.restaurantAssert.assertProductNotInList()
        self.restaurantAssert.assertStornoSucces(data.Product['Babgulyás']['Name'])

        # mennyiseg ellenorzese
        self.stockAssert.assertStock(data.RawMaterial['Bundas_kenyer']['Name'],
                                     data.RawMaterial['Bundas_kenyer']['Warehouse'], '10')

    def testUnion(self):
        inputName = data.Product['Babgulyás']['Name']

        for i in range(10):
            self.addProductToList(inputName, '1.00')

        #self.html.clickElement('aaaa', 'div') # ez a verzi nem az elso elemet jelolte ki
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', inputName)
        self.html.clickElement('Összevonás', waitSeconds=2)
        for i in range(4):
            self.html.clickElement('unionMinus', 'a', options=Options(htmlAttribute='id'))
        self.html.wait(3)
        self.html.clickElement('Összevonás / Áthelyezés', waitSeconds=4)

        # csekkolás
        for i in range(2, 7):
            tempName = self.html.getTxtFromListTable2(str(i), '3')
            tempQty = self.html.getTxtFromListTable2(str(i), '5')

            self.assertEqual(tempName.text, inputName)
            if i == 2:
                self.assertEqual(tempQty.text, '6.00')
            else:
                self.assertEqual(tempQty.text, '1.00')

        # törlés
        self.html.clickElement('Minden összevonása', waitSeconds=4)
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', 'Törlés')
        self.html.clickElement('Igen', waitSeconds=2)
        # itt azt csekkoljuk hogy a rendeles bekuldese gomb eltunt e
        self.assertFalse(self.html.getElement('Rendelés beküldése', 'button').is_displayed())

    def testUnfold(self):
        self.html.wait(10)
        inputName = data.Product['Babgulyás']['Name']

        self.addProductToList(inputName, '10.00')

        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', inputName)
        self.html.clickElement('Bontás', waitSeconds=2)
        for i in range(4):
            self.html.clickElement('unfoldMinus', 'a', options=Options(htmlAttribute='id'))

        self.html.wait(3)
        self.html.clickElement('Bontás / Áthelyezés', waitSeconds=4)

        name = self.html.getTxtFromListTable2('2', '3')
        name2 = self.html.getTxtFromListTable2('3', '3')
        qty = self.html.getTxtFromListTable2('2', '5')
        qty2 = self.html.getTxtFromListTable2('3', '5')

        self.assertEqual(name.text, inputName)
        self.assertEqual(qty.text, '6.00')
        self.assertEqual(name2.text, inputName)
        self.assertEqual(qty2.text, '4.00')

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

        name = self.html.getTxtFromListTable2('2', '3')
        name2 = self.html.getTxtFromListTable2('3', '3')
        qty = self.html.getTxtFromListTable2('2', '5')
        qty2 = self.html.getTxtFromListTable2('3', '5')

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
        self.html.refresh()

        self.html.clickElement('Rendelés beküldése', waitSeconds=3)
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        # művelet
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', inputName)
        self.html.clickElement('Áthelyez részasztalra')
        partTablesDialog = self.html.getElement('moveDialog', 'div', options=Options(htmlAttribute='id'))
        self.html.clickElement('2', 'a', options=Options(element=partTablesDialog), waitSeconds=4)

        self.html.clickElement('2', 'a')

        # csekkolas
        name = self.html.getTxtFromListTable2('2', '3')
        qty = self.html.getTxtFromListTable2('2', '5')
        self.assertEqual(name.text, inputName)
        self.assertEqual(qty.text, '1.00')

        # sztorno
        self.html.clickElement('Sztornó', 'a')
        self.html.clickElement('Vendég visszamondta (raktárba visszatesz)', waitSeconds=2)
        self.html.wait(5)  # megkell varni h az ertesitesi ablak megjelenjen
        self.assertTrue(
            self.html.getElement(inputName + ' nevű termék a felszolgáló által sztornózva lett! ', 'li').is_displayed())
        self.html.clickElement('Rendben', 'a')

        self.html.clickElement('1', 'a')

    def testMoveToTable(self):
        inputName = data.Product['Babgulyás']['Name']
        inputName2 = data.Product['Palacsinta']['Name']

        self.addProductToList(inputName, '1.00')
        self.addProductToList(inputName2, '1.00')
        self.html.refresh()

        self.html.clickElement('Rendelés beküldése', waitSeconds=3)
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        # muvelet
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName, 'div', inputName)
        self.html.clickElement('Áthelyez másik asztalra')
        self.html.clickElement(data.Table['Courier']['Name'], 'a')

        self.html.refresh()
        self.html.clickElement('Vissza', 'a', waitSeconds=2)
        self.html.clickElement(data.Table['Courier']['Name'], tag='i')

        # csekkoljuk a dolgokat
        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))
        self.assertEqual(name.text, inputName)
        self.assertEqual(qty.text, '1.00')

        # sztorno
        self.html.clickElement('Sztornó', 'a')
        self.html.clickElement('Vendég visszamondta (raktárba visszatesz)', waitSeconds=2)
        self.restaurantAssert.assertStornoSucces(inputName)

        self.html.clickElement('Vissza', 'a')
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.html.clickElement('Sztornó', 'a')
        self.html.clickElement('Vendég visszamondta (raktárba visszatesz)', waitSeconds=2)
        self.restaurantAssert.assertStornoSucces(inputName2)

    def testMoveToReservedTable(self):
        inputName = data.Product['Babgulyás']['Name']
        inputName2 = data.Product['Palacsinta']['Name']

        # elso asztalra rendeles bekuldese
        self.addProductToList(inputName, '1.00')
        self.html.refresh()
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)
        self.html.clickElement(data.Table['Courier']['Name'], tag='i')

        # masodik asztalra rendeles bekuldese
        self.addProductToList(inputName, '1.00')
        self.addProductToList(inputName2, '1.00')
        self.html.refresh()
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)
        self.html.clickElement(data.Table['Courier']['Name'], tag='i')

        # muvelet
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', inputName2, 'div', inputName2)
        self.html.clickElement('Áthelyez másik asztalra')
        self.html.clickElement(data.Table['Normal']['Name'], 'a', waitSeconds=2)

        self.html.clickElement('Vissza', 'a', waitSeconds=2)
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        #
        # ide talan kene assert h melyik asztalon is vagyunk

        # csekkoljuk a dolgokat az elso asztalon, ahova athelyeztuk a termeket

        # csekkolas

        name2 = self.html.getTxtFromListTable2('2', '3')
        qty2 = self.html.getTxtFromListTable2('2', '5')
        self.assertEqual(name2.text, inputName)
        self.assertEqual(qty2.text, '1.00')
        self.html.clickElement('Sztornó', 'a')
        self.html.clickElement('Vendég visszamondta (raktárba visszatesz)', waitSeconds=2)
        self.restaurantAssert.assertStornoSucces(inputName)

        self.html.clickElement('2', 'a', waitSeconds=2)
        name = self.html.getTxtFromListTable2('2', '3')
        qty = self.html.getTxtFromListTable2('2', '5')

        self.assertEqual(name.text, inputName2)
        self.assertEqual(qty.text, '1.00')
        self.html.clickElement('Sztornó', 'a')
        self.html.clickElement('Vendég visszamondta (raktárba visszatesz)', waitSeconds=2)
        self.restaurantAssert.assertStornoSucces(inputName2)

        # vissza a 2. asztalra
        self.html.clickElement('Vissza', 'a', waitSeconds=2)
        self.html.clickElement(data.Table['Courier']['Name'], 'a')

        # csekkoljuk a 3. asztalon is a dolgokat
        name3 = self.html.getTxtFromListTable2('2', '3')
        qty3 = self.html.getTxtFromListTable2('2', '5')
        self.assertEqual(name3.text, inputName)
        self.assertEqual(qty3.text, '1.00')

        # sztorno
        self.html.clickElement('Sztornó', 'a')
        self.html.clickElement('Vendég visszamondta (raktárba visszatesz)', waitSeconds=2)
        self.restaurantAssert.assertStornoSucces(inputName)
















