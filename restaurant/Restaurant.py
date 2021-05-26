''' Na ez hosszu menet lesz...'''
import unittest

from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options


class Restaurant(BaseTestCase):
    rawMaterials = ['Csirkemell', 'Finomliszt', 'Almalé', 'Hasábburgonya', 'Sonka', 'Paradicsomszósz']

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
        for material in self.rawMaterials:
            self.stockseed.createRawMaterialWithOpening(data.RawMaterial[material]['Name'],
                                                        data.RawMaterial[material]['GrosPrice'],
                                                        data.RawMaterial[material]['Quantity'],
                                                        data.RawMaterial[material]['Warehouse'],
                                                        data.RawMaterial[material]['ME'],
                                                        module=True)

        self.productseed.createCounter(data.Counter['TestCounter']['Name'], data.Counter['TestCounter']['Position'],
                                       module=True)
        #self.productseed.createProductGroup(data.ProductGroup['Egyeb']['Name'], tab=True)
        #self.html.wait(5)
        # self.productseed.createProductGroup(data.ProductGroup['Öntetek']['Name'])
        self.productseed.createProduct(data.Product['Babgulyás']['Name'], data.ProductGroup['Egyeb']['Name'],
                                       data.Product['Babgulyás']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.productseed.createProduct(data.Product['Palacsinta']['Name'], data.ProductGroup['Egyeb']['Name'],
                                       data.Product['Palacsinta']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Bundas_kenyer']['Name'], module=True)

        self.productseed.createProduct(data.Product['Hasábburgonya']['Name'], 'Köretek',
                                       data.Product['Hasábburgonya']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Hasábburgonya']['Name'],
                                       data.Product['Hasábburgonya']['Quantity'],
                                       data.Product['Hasábburgonya']['NetPrice'], module=True)

        self.productseed.createProduct('Almalé', 'Kiszereléses',
                                       '99', data.Counter['TestCounter']['Name'], data.RawMaterial['Almalé']['Name'],
                                       '1', '2200',
                                       module=True)

        self.productseed.createProduct(data.Product['Sonka']['Name'], data.Product['Sonka']['ProductGroup'],
                                       data.Product['Sonka']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Sonka']['Name'], data.Product['Sonka']['Quantity'],
                                       data.Product['Sonka']['NetPrice'],
                                       module=True)

        self.productseed.createProduct(data.Product['Paradicsomszósz']['Name'],
                                       data.Product['Paradicsomszósz']['ProductGroup'],
                                       data.Product['Paradicsomszósz']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Paradicsomszósz']['Name'],
                                       data.Product['Paradicsomszósz']['Quantity'], '0',
                                       module=True)
        self.menu.openProducts()
        self.productseed.createProductChose('Roston csirkemell')
        self.productseed.createProductFix('Rántott csirkemell', 'Hasábburgonya', module=True)
        self.productseed.createProductAsRawMaterial(module=True)
        self.productseed.createSpecialPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'],
                                            data.Product['Sonka']['Name'], module=True)

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

    @classmethod
    def tearDownClass(self):
        self.restaurantseed.deleteTable(data.Table['Normal']['Name'], module=True)
        self.restaurantseed.deleteTable(data.Table['Courier']['Name'], module=True)
        super().tearDownClass()

    def tearDown(self):
        print('TEARDOWN')
        self.productseed.deleteProduct(data.Product['Babgulyás']['Name'], module=True)
        self.productseed.deleteProduct(data.Product['Palacsinta']['Name'], module=True)
        self.productseed.deleteCounter(data.Counter['TestCounter']['Name'], tab=True)
        self.productseed.deleteProduct(data.Product['Hasábburgonya']['Name'], module=True)
        self.productseed.deleteProduct('Roston csirkemell', module=True)
        self.productseed.deleteProduct('Rántott csirkemell', module=True)
        #self.productseed.deleteProduct('Almalé')
        self.productseed.deleteProduct('Kóla', module=True)
        self.productseed.deleteProduct(data.Product['Sonka']['Name'], module=True)
        self.productseed.deleteProduct(data.Product['Paradicsomszósz']['Name'], module=True)
        self.productseed.deletePizza('Sonkás pizza', module=True)
        #self.productseed.deleteCounter(data.Counter['TestCounter']['Name'], tab=True)

        self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Alma']['Name'], module=True)
        for material in self.rawMaterials:
            self.stockseed.deleteRawMaterial(data.RawMaterial[material]['Name'], module=True)
        self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)

    def addProductToList(self, productName, quantity):
        self.html.fillAutocomplete('Terméknév', 'input', productName[:-1], productName, 'li',
                                   Options(htmlAttribute='placeholder'))

        self.html.fillInput('Mennyiség', quantity, 'placeholder')
        self.html.clickElement('addProduct', 'a', options=Options(htmlAttribute='id'))
        name = self.html.getTxtFromListTable('2', '3', tableId='tasks-list products ui-sortable',
                                             options=Options(htmlAttribute='class'))
        qty = self.html.getTxtFromListTable('2', '5', tableId='tasks-list products ui-sortable',
                                            options=Options(htmlAttribute='class'))

        self.assertEqual(name.text, productName)
        self.assertEqual(qty.text, quantity)

    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
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

    # assert ertek hiba(1 a kulonbseg)
    @unittest.skip
    def testMultipleOrders(self):
        self.menu.openFinance()
        try:
            startValue = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2]
        except Exception as e:
            startValue = '0 0'
        # print(startValue)

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.html.clickElement('Pizza (testreszabható)', 'a')
        self.html.wait(1)
        self.html.clickElement('Sonkás pizza', 'span')
        self.html.wait(1)
        # self.html.clickElement(None,
        #                       '//div[@id="pizzaCustomizeDialog"]//span',
        #                      Options(uniqueSelector=True))
        # self.html.clickElement('pizzaCustomizeDialog', 'div', Options(htmlAttribute='id', following='span/span/span'))
        # self.html.clickElement('Rögzít')
        self.html.refresh()
        self.addProductToList('Rántott csirkemell', '1.00')

        self.html.clickElement('Ital', 'a')
        self.html.wait(2)
        self.html.clickElement('Üdítők', 'a')
        self.html.wait(2)
        # self.html.clickElement('Kóla', 'span')
        self.html.clickElement('Kóla', 'span', options=Options(exactMatch=True))
        self.html.wait(2)

        # self.html.clickElement('Kiszereléses', 'a')
        # self.html.wait(2)
        # self.html.clickElement('Almalé', 'a')
        # self.html.switchFrame('iframe')
        # ActionChains(self.driver).move_by_offset(400, 130).click().perform()
        # self.html.switchFrame()
        # self.html.wait(2)

        self.addProductToList('Roston csirkemell', '1.00')
        self.html.wait(2)
        self.html.wait(2)
        # self.html.clickElement('Hasábburgonya','label')
        # self.html.clickElement('sideDishSaveButton', 'button', Options(htmlAttribute='id'))
        # self.html.switchFrame('iframe')

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.html.wait(2)
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)

        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.html.clickElement('Fizetés')

        # self.html.getElement('sum', 'span', Options(htmlAttribute='class'))
        price = self.html.getElement('Összesen', 'h2', Options(following='span')).text.split('.')[0]
        # print(price)

        self.html.clickElement('Kitölt')

        self.html.clickElement('payDialogButton', 'button', Options(htmlAttribute='id'))
        stvalue = startValue.split(' ')
        prc = price.split(' ')
        prcInt = int(prc[0] + prc[1])
        expected = int(stvalue[0] + stvalue[1]) + prcInt
        # print('ex '+ str(expected))
        self.menu.openFinance()
        self.html.refresh()
        self.html.wait()
        actual = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2].split(' ')
        actInt = int(actual[0] + actual[1])
        # print('act ' + str(actInt))

        self.assertEqual(expected, actInt)

    # kozbe jo kozbe nem
    @unittest.skip
    def testMultipleOrdersCredit(self):
        self.menu.openFinance()
        try:
            startValue = self.html.getElement('Bankkártya', 'td', Options(following='td')).text[:-2]
        except:
            startValue = '0 0'

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.html.clickElement('Pizza (testreszabható)', 'a')
        self.html.wait(1)
        self.html.clickElement('Sonkás pizza', 'span')

        self.menu.openRestaurant()

        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.addProductToList('Rántott csirkemell', '1.00')

        self.html.clickElement('Pizza (testreszabható)', 'a')
        self.html.wait(10)
        self.html.clickElement('Sonkás pizza', 'span')
        self.html.wait(2)
        self.html.refresh()

        self.html.clickElement('Ital', 'a')
        self.html.wait(2)
        self.html.clickElement('Üdítők', 'a')
        self.html.wait(10)
        #self.html.clickElement('Kóla', 'span')
        self.html.clickElement('Kóla', 'span', options=Options(exactMatch=True))

        self.addProductToList('Roston csirkemell', '1.00')
        self.html.wait(2)
        #self.html.clickElement('Hasábburgonya','label')
        #self.html.clickElement('sideDishSaveButton', 'button', Options(htmlAttribute='id'))

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.html.wait(2)
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)

        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.html.clickElement('Fizetés')

        #self.html.getElement('sum', 'span', Options(htmlAttribute='class'))
        price = self.html.getElement('Összesen', 'h2', Options(following='span')).text.split('.')[0]
        print(price)

        self.html.clickElement('Bankkártya', 'td', Options(following='button'))

        self.html.clickElement('payDialogButton', 'button', Options(htmlAttribute='id'))
        stvalue = startValue.split(' ')
        prc = price.split(' ')
        prcInt = int(prc[0] + prc[1])
        expected = int(stvalue[0]+stvalue[1]) + prcInt
        self.menu.openFinance()
        self.html.refresh()
        self.html.wait()
        actual = self.html.getElement('Bankkártya', 'td', Options(following='td')).text[:-2].split(' ')
        actInt = int(actual[0] + actual[1])

        self.assertEqual(expected, actInt)
        #self.html.switchFrame('iframe')

    @unittest.skip
    def testInstantPayment(self):
        self.menu.openFinance()
        try:
            startValue = self.html.getElement('Bankkártya', 'td', Options(following='td')).text[:-2]
        except:
            startValue = '0 0'

        self.menu.openRestaurant()

        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.addProductToList('Rántott csirkemell', '1.00')

        self.html.clickElement('Pizza (testreszabható)', 'a')
        self.html.wait(1)
        self.html.clickElement('Sonkás pizza', 'span')
        self.html.wait(1)
        self.html.refresh()

        self.html.clickElement('Ital', 'a')
        self.html.wait(2)
        self.html.clickElement('Üdítők', 'a')
        self.html.wait(10)
        #self.html.clickElement('Kóla', 'span')
        self.html.clickElement('Kóla', 'span', options=Options(exactMatch=True))

        self.addProductToList('Roston csirkemell', '1.00')
        self.html.wait(2)
        # self.html.clickElement('Hasábburgonya','label')
        # self.html.clickElement('sideDishSaveButton', 'button', Options(htmlAttribute='id'))

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.html.wait(2)
        #self.html.clickElement('Rendelés beküldése', waitSeconds=3)

        #self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.html.clickElement('Azonnali fizetés')

        # self.html.getElement('sum', 'span', Options(htmlAttribute='class'))
        price = self.html.getElement('Összesen', 'h2', Options(following='span')).text.split('.')[0]
        print(price)

        self.html.clickElement('Bankkártya', 'td', Options(following='button'))

        self.html.clickElement('payDialogButton', 'button', Options(htmlAttribute='id'))
        stvalue = startValue.split(' ')
        prc = price.split(' ')
        prcInt = int(prc[0] + prc[1])
        expected = int(stvalue[0] + stvalue[1]) + prcInt
        self.menu.openFinance()
        self.html.refresh()
        self.html.wait()
        actual = self.html.getElement('Bankkártya', 'td', Options(following='td')).text[:-2].split(' ')
        actInt = int(actual[0] + actual[1])

        self.assertEqual(expected, actInt)

    def testDiscountedTable(self):
        self.restaurantseed.createTable('Kedvezmeny', 'Kör', 'Személyzeti', '10', module=True)

        self.menu.openFinance()
        try:
            startValue = self.html.getElement('Bankkártya', 'td', Options(following='td')).text[:-2]
        except:
            startValue = '0 0'

        self.menu.openRestaurant()

        self.html.clickElement('Kedvezmeny', tag='i')
        self.addProductToList('Rántott csirkemell', '1.00')

        self.html.clickElement('Pizza (testreszabható)', 'a')
        self.html.wait(1)
        self.html.clickElement('Sonkás pizza', 'span')
        self.html.wait(1)
        self.html.refresh()

        self.html.clickElement('Ital', 'a')
        self.html.wait(2)
        self.html.clickElement('Üdítők', 'a')
        print('ADD COLA')
        print(self.driver.current_url)
        self.html.wait(10)
        self.html.clickElement('Kóla', 'span', options=Options(exactMatch=True))

        self.addProductToList('Roston csirkemell', '1.00')
        self.html.wait(2)
        # self.html.clickElement('Hasábburgonya','label')
        # self.html.clickElement('sideDishSaveButton', 'button', Options(htmlAttribute='id'))

        self.menu.openRestaurant()
        self.html.clickElement('Kedvezmeny', tag='i')
        print('RENDELES BEKULDESE')
        print(self.driver.current_url)
        self.html.wait(2)
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)

        self.html.clickElement('Kedvezmeny', tag='i')
        self.html.clickElement('Fizetés')

        # self.html.getElement('sum', 'span', Options(htmlAttribute='class'))
        price = self.html.getElement('Összesen', 'h2', Options(following='span')).text.split('.')[0]
        print(price)

        print('BANKKARTYA')
        print(self.driver.current_url)
        self.html.clickElement('Bankkártya', 'td', Options(following='button'))

        self.html.clickElement('payDialogButton', 'button', Options(htmlAttribute='id'))
        stvalue = startValue.split(' ')
        prc = price.split(' ')
        prcInt = int(prc[0] + prc[1])
        expected = int(stvalue[0] + stvalue[1]) + prcInt
        self.menu.openFinance()
        self.html.refresh()
        self.html.wait()
        actual = self.html.getElement('Bankkártya', 'td', Options(following='td')).text[:-2].split(' ')
        actInt = int(actual[0] + actual[1])

        self.assertEqual(expected, actInt)

        self.restaurantseed.deleteTable('Kedvezmeny', module=True)

    def testTake(self):
        self.restaurantseed.createTable('Elvitel', 'Kör', 'Elvitel', '10', module=True)

        self.menu.openFinance()
        try:
            startValue = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2]
        except:
            startValue = '0 0'

        self.menu.openRestaurant()

        self.html.clickElement('Elvitel', tag='i')
        self.addProductToList('Rántott csirkemell', '1.00')

        self.html.clickElement('Pizza (testreszabható)', 'a')
        self.html.wait(1)
        self.html.clickElement('Sonkás pizza', 'span')
        self.html.wait(1)
        self.html.refresh()

        self.html.clickElement('Ital', 'a')
        self.html.wait(2)
        self.html.clickElement('Üdítők', 'a')
        self.html.wait(2)
        #self.html.clickElement('Kóla', 'span')
        self.html.clickElement('Kóla', 'span', options=Options(exactMatch=True))

        self.addProductToList('Roston csirkemell', '1.00')
        self.html.wait(2)
        # self.html.clickElement('Hasábburgonya','label')
        # self.html.clickElement('sideDishSaveButton', 'button', Options(htmlAttribute='id'))

        self.menu.openRestaurant()
        self.html.clickElement('Elvitel', tag='i')
        self.html.wait(2)
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)

        self.html.clickElement('Elvitel', tag='i')
        self.html.clickElement('Fizetés')

        # self.html.getElement('sum', 'span', Options(htmlAttribute='class'))
        price = self.html.getElement('Összesen', 'h2', Options(following='span')).text.split('.')[0]
        print(price)

        self.html.clickElement('Készpénz', 'td', Options(following='button'))

        self.html.clickElement('payDialogButton', 'button', Options(htmlAttribute='id'))
        stvalue = startValue.split(' ')
        prc = price.split(' ')
        prcInt = int(prc[0] + prc[1])
        expected = int(stvalue[0] + stvalue[1]) + prcInt
        self.html.wait(5)
        self.menu.openFinance()
        self.html.refresh()
        self.html.wait()
        actual = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2].split(' ')
        actInt = int(actual[0] + actual[1])

        self.assertEqual(expected, actInt)
        self.assertEqual(expected, actInt)

        self.restaurantseed.deleteTable('Elvitel', module=True)














'''
    def addProductToList(self, productName, quantity):
        self.html.fillAutocomplete('Terméknév', 'input', productName[:-1], productName, 'li',
                                   Options(htmlAttribute='placeholder'))

        self.html.fillInput('Mennyiség', quantity, 'placeholder')
        self.html.clickElement('addProduct', 'a', options=Options(htmlAttribute='id'))
        name = self.html.getTxtFromListTable2('2', '3')
        qty = self.html.getTxtFromListTable2('2', '5')

        self.assertEqual(name.text, productName)
        self.assertEqual(qty.text, quantity)
'''
