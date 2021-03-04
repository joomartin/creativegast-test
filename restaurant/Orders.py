from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options
from selenium.webdriver.common.action_chains import ActionChains
from restaurant.Restaurant import Restaurant


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
                                                    data.RawMaterial['Finomliszt']['Warehouse'], data.RawMaterial['Finomliszt']['ME'], module=True)

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

        self.productseed.createProduct(data.Product['Sonka']['Name'], data.Product['Sonka']['ProductGroup'],
                                       data.Product['Sonka']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Sonka']['Name'], data.Product['Sonka']['Quantity'], data.Product['Sonka']['NetPrice'], module=True)

        self.productseed.createProduct(data.Product['Paradicsomszósz']['Name'],
                                       data.Product['Paradicsomszósz']['ProductGroup'],
                                       data.Product['Paradicsomszósz']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Paradicsomszósz']['Name'], data.Product['Paradicsomszósz']['Quantity'], '0', module=True)

        '''
        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        '''
        self.menu.openProducts()

    @classmethod
    def tearDownClass(self):
        self.restaurantseed.deleteTable(data.Table['Normal']['Name'], module=True)
        super().tearDownClass()

    def tearDown(self):

        self.productseed.deleteProduct(data.Product['Hasábburgonya']['Name'], module=True)
        self.productseed.deleteProduct('Roston csirkemell')
        self.productseed.deleteProduct('Rántott csirkemell')
        self.productseed.deleteProduct('Almalé')
        self.productseed.deleteProduct('Kóla')
        self.productseed.deleteProduct(data.Product['Sonka']['Name'])
        self.productseed.deleteProduct(data.Product['Paradicsomszósz']['Name'])
        self.productseed.deletePizza('Sonkás pizza', module=True)
        self.productseed.deleteCounter(data.Counter['TestCounter']['Name'], tab=True)

        self.stockseed.deleteRawMaterial(data.RawMaterial['Csirkemell']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Finomliszt']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Almalé']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Hasábburgonya']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Sonka']['Name'], module=True)
        self.stockseed.deleteRawMaterial(data.RawMaterial['Paradicsomszósz']['Name'], module=True)
        self.stockseed.deleteRawMaterial('Kóla', module=True)
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

    def createProductAsRawMaterial(self):
        self.menu.openProducts()

        self.html.clickElement('Új termék felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', 'Pult')
        self.html.switchFrame('iframe')

        self.html.clickElement('Üdítők', 'a')
        self.html.clickElement('Rögzít')
        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', 'Kóla')
        places = self.html.getElement('Eladási ár (Kötelező)', 'td')
        self.html.clickElement('Ár megadása', options=Options(element=places))
        self.html.fillInput('Nettó', '300')
        self.html.wait(1)
        self.html.clickElement('taxPriceSave', 'a', options=Options(htmlAttribute='id'))
        self.html.wait(2)

        self.html.clickElement('Felvétel nyersanyagként', 'label', Options(following='i'))

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


        self.assertEqual(name.text, productName)
        self.assertEqual(qty.text, quantity)

    def testMultipleOrders(self):
        self.menu.openFinance()
        try:
            startValue = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2]
        except:
            startValue = '0 0'
        print(startValue)
        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()

        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openRestaurant()

        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.html.clickElement('Pizza (testreszabható)', 'a')
        self.html.wait(1)
        self.html.clickElement('Sonkás pizza', 'span')
        self.html.wait(1)
       # self.html.clickElement(None,
        #                       '//div[@id="pizzaCustomizeDialog"]//span',
        #                      Options(uniqueSelector=True))
        #self.html.clickElement('pizzaCustomizeDialog', 'div', Options(htmlAttribute='id', following='span/span/span'))
        #self.html.clickElement('Rögzít')
        self.html.refresh()
        self.addProductToList('Rántott csirkemell', '1.00')


        self.html.clickElement('Ital', 'a')
        self.html.wait(2)
        self.html.clickElement('Üdítők', 'a')
        self.html.wait(2)
        self.html.clickElement('Kóla', 'span')
        self.html.wait(2)

        '''
        self.html.clickElement('Kiszereléses', 'a')
        self.html.wait(2)
        self.html.clickElement('Almalé', 'a')
        self.html.switchFrame('iframe')
        ActionChains(self.driver).move_by_offset(400, 130).click().perform()
        self.html.switchFrame()
        self.html.wait(2)
        '''

        self.addProductToList('Roston csirkemell', '1.00')
        self.html.wait(2)
        self.html.wait(2)
        #self.html.clickElement('Hasábburgonya','label')
        #self.html.clickElement('sideDishSaveButton', 'button', Options(htmlAttribute='id'))
        # self.html.switchFrame('iframe')

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.html.wait(2)
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)

        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.html.clickElement('Fizetés')

        #self.html.getElement('sum', 'span', Options(htmlAttribute='class'))
        price = self.html.getElement('Összesen', 'h2', Options(following='span')).text.split('.')[0]
        print(price)

        self.html.clickElement('Kitölt')

        self.html.clickElement('payDialogButton', 'button', Options(htmlAttribute='id'))
        stvalue = startValue.split(' ')
        prc= price.split(' ')
        prcInt = int(prc[0] + prc[1])
        expected = int(stvalue[0]+stvalue[1]) + prcInt
        print('ex '+ str(expected))
        self.menu.openFinance()
        self.html.refresh()
        self.html.wait()
        actual = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2].split(' ')
        actInt=int(actual[0] + actual[1])
        print('act ' + str(actInt))

        self.assertEqual(expected, actInt)

    def testMultipleOrdersCredit(self):
        self.menu.openFinance()
        try:
            startValue = self.html.getElement('Bankkártya', 'td', Options(following='td')).text[:-2]
        except:
            startValue = '0 0'

        print(startValue)
        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()
        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openRestaurant()

        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.addProductToList('Rántott csirkemell', '1.00')

        self.html.clickElement('Pizza (testreszabható)', 'a')
        self.html.wait(1)
        self.html.clickElement('Sonkás pizza', 'span')
        self.html.wait(1)

        self.html.clickElement('Ital', 'a')
        self.html.wait(2)
        self.html.clickElement('Üdítők', 'a')
        self.html.wait(2)
        self.html.clickElement('Kóla', 'span')

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
        self.assertEqual(expected, actInt)
        #self.html.switchFrame('iframe')

    def testInstantPayment(self):
        self.menu.openFinance()
        try:
            startValue = self.html.getElement('Bankkártya', 'td', Options(following='td')).text[:-2]
        except:
            startValue = '0 0'

        print(startValue)
        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()
        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

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
        self.html.wait(2)
        self.html.clickElement('Kóla', 'span')

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
        self.assertEqual(expected, actInt)

    def createPizza(self, pizzaName, baseComponent, topping, module=False, tab=False):
        if module:
            self.menu.openProducts()
            self.html.clickElement('Pizza (testreszabható)', 'a')
        elif tab:
            self.html.clickElement('Pizza (testreszabható)', 'a')

        self.html.clickElement('Új pizza (testreszabható)', 'a')

        self.html.switchFrame('iframe')
        self.html.clickDropdown('Nyomtatási részleg', 'Pizza')
        self.html.fillInput('Termék neve', pizzaName)
        self.html.fillInput('Kód', '1333')

        self.html.clickDropdown('Szósz', 'Paradicsomszósz')

        self.html.fillAutocomplete('baseComponentName', 'input', baseComponent, baseComponent, 'li',
                                   Options(htmlAttribute='id'))
        table = self.html.getElement('baseComponents', 'table', Options(htmlAttribute='id'))
        self.html.getElement('Hozzáad', 'button', Options(element=table)).click()

        self.html.fillAutocomplete('toppingComponentName', 'input', topping, topping, 'li',
                                   Options(htmlAttribute='id'))
        table = self.html.getElement('toppingComponents', 'table', Options(htmlAttribute='id'))
        self.html.getElement('Hozzáad', 'button', options=Options(element=table)).click()

        self.html.clickElement('Mennyiségek', 'a')
        self.html.wait(2)

        self.html.clickElement('edit actionButton fright editPriceBtn', 'a', Options(htmlAttribute='class'))
        self.html.fillInput('grossPrice-2-1', '1400', 'input', options=Options(htmlAttribute='name'))
        self.html.fillInput('grossPrice-5-1', '2000', 'input', options=Options(htmlAttribute='name'))
        self.html.wait(2)
        self.html.clickElement('Rögzít', 'a', waitSeconds=2)
        self.html.clickElement('Rögzít')

        self.html.clickTableElement('customproduct-2', 'id', 'Sonkás pizza', 'a', 'Szerkeszt',
                                    'Pizza (testreszabható)')
        self.html.switchFrame('iframe')
        self.html.clickElement('Mennyiségek', 'a')
        self.html.wait(2)
        inputFields = self.html.getElements('inputmask-numeric qtys', 'input',
                                            options=Options(htmlAttribute='class'))

        inputFields[0].send_keys('0,18')
        inputFields[1].send_keys('0,18')
        # self.html.fillInput('inputmask-numeric qtys', '0,18', 'input', options=Options(htmlAttribute='class', element=inputFields[0]))
        # self.html.fillInput('inputmask-numeric qtys', '0,18', 'input', options=Options(htmlAttribute='class', element=inputFields[1]))
        self.html.clickElement('Rögzít')

    def testDiscountedTable(self):
        self.restaurantseed.createTable('Kedvezmeny','Kör','Személyzeti','10', module=True)

        self.menu.openFinance()
        try:
            startValue = self.html.getElement('Bankkártya', 'td', Options(following='td')).text[:-2]
        except:
            startValue = '0 0'

        print(startValue)
        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()
        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

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
        self.html.wait(2)
        self.html.clickElement('Kóla', 'span')

        self.addProductToList('Roston csirkemell', '1.00')
        self.html.wait(2)
        # self.html.clickElement('Hasábburgonya','label')
        # self.html.clickElement('sideDishSaveButton', 'button', Options(htmlAttribute='id'))

        self.menu.openRestaurant()
        self.html.clickElement('Kedvezmeny', tag='i')
        self.html.wait(2)
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)

        self.html.clickElement('Kedvezmeny', tag='i')
        self.html.clickElement('Fizetés')

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
        self.assertEqual(expected, actInt)

        self.restaurantseed.deleteTable('Kedvezmeny',module=True)

    def testTake(self):
        self.restaurantseed.createTable('Elvitel','Kör','Elvitel','10', module=True)

        self.menu.openFinance()
        try:
            startValue = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2]
        except:
            startValue = '0 0'

        print(startValue)
        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()
        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

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
        self.html.clickElement('Kóla', 'span')

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
        self.menu.openFinance()
        self.html.refresh()
        self.html.wait()
        actual = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2].split(' ')
        actInt = int(actual[0] + actual[1])

        self.assertEqual(expected, actInt)
        self.assertEqual(expected, actInt)

        self.restaurantseed.deleteTable('Elvitel', module=True)

    '''
    def testCustomizable(self):
        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         tab=True)

        # assert
        self.productAssert.assertPizzaExists('Sonkás pizza', '1400.00')
        self.html.clickTableElement('customproduct-2', 'id', 'Sonkás pizza', 'a', 'Részletek',
                                    'Pizza (testreszabható)')
        self.html.switchFrame('iframe')
        # self.assertTrue(self.html.getElement('Paradicsomszósz', 'button').is_displayed())

        # self.assertTrue(self.html.getElement('Finomliszt', 'td').is_displayed())

        baseName = self.html.getTxtFromTable('3', '1', tableId='baseQuantities')
        littleQty = self.html.getTxtFromTable('3', '2', tableId='baseQuantities')
        bigQty = self.html.getTxtFromTable('3', '3', tableId='baseQuantities')
        self.assertEqual(baseName, 'Finomliszt')
        self.assertEqual(littleQty[:4], '0.18')
        self.assertEqual(bigQty[:4], '0.18')
        self.html.refresh()

        self.productseed.deletePizza('Sonkás pizza')
        '''





