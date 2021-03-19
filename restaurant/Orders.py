import unittest

from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options
from selenium.webdriver.common.action_chains import ActionChains
from restaurant.Restaurant import Restaurant


class Orders(BaseTestCase):
    name = data.Client['Pista']['Name']
    code = data.Client['Pista']['Code']
    phone = data.Client['Pista']['Phone']
    discount = data.Client['Pista']['Discount']
    taxnumber = data.Client['Pista']['TaxNumber']
    country = data.Client['Pista']['Country']
    postalCode = data.Client['Pista']['PostalCode']
    city = data.Client['Pista']['City']
    street = data.Client['Pista']['Street']
    housenumber = data.Client['Pista']['HouseNumber']
    address = None

    days = ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap']

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)
        self.restaurantseed.createTable(data.Table['Normal']['Name'], module=True)
        self.restaurantseed.createTable(data.Table['Courier']['Name'], module=True)

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
                                                    data.RawMaterial['Finomliszt']['Warehouse'], data.RawMaterial['Finomliszt']['ME'],
                                                    module=True)

        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Almalé']['Name'],
                                                    data.RawMaterial['Almalé']['GrosPrice'],
                                                    data.RawMaterial['Almalé']['Quantity'],
                                                    data.RawMaterial['Almalé']['Warehouse'],
                                                    data.RawMaterial['Almalé']['ME'],
                                                    module=True)

        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Hasábburgonya']['Name'],
                                                    data.RawMaterial['Hasábburgonya']['GrosPrice'],
                                                    data.RawMaterial['Hasábburgonya']['Quantity'],
                                                    data.RawMaterial['Hasábburgonya']['Warehouse'],
                                                    data.RawMaterial['Hasábburgonya']['ME'],
                                                    module=True)

        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Sonka']['Name'],
                                                    data.RawMaterial['Sonka']['GrosPrice'],
                                                    data.RawMaterial['Sonka']['Quantity'],
                                                    data.RawMaterial['Sonka']['Warehouse'],
                                                    data.RawMaterial['Sonka']['ME'],
                                                    module=True)

        self.stockseed.createRawMaterialWithOpening(data.RawMaterial['Paradicsomszósz']['Name'],
                                                    data.RawMaterial['Paradicsomszósz']['GrosPrice'],
                                                    data.RawMaterial['Paradicsomszósz']['Quantity'],
                                                    data.RawMaterial['Paradicsomszósz']['Warehouse'],
                                                    data.RawMaterial['Paradicsomszósz']['ME'],
                                                    module=True)

        self.productseed.createCounter(data.Counter['TestCounter']['Name'], data.Counter['TestCounter']['Position'],
                                       module=True)
        #self.productseed.createProductGroup(data.ProductGroup['Egyeb']['Name'], tab=True)
        self.html.wait(5)
        self.productseed.createProduct(data.Product['Hasábburgonya']['Name'], 'Köretek',
                                       data.Product['Hasábburgonya']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Hasábburgonya']['Name'], data.Product['Hasábburgonya']['Quantity'],
                                       data.Product['Hasábburgonya']['NetPrice'], module=True)

        self.productseed.createProduct('Almalé', 'Kiszereléses',
                                       '99', data.Counter['TestCounter']['Name'], data.RawMaterial['Almalé']['Name'], '1', '2200',
                                       module=True)

        self.productseed.createProduct(data.Product['Sonka']['Name'], data.Product['Sonka']['ProductGroup'],
                                       data.Product['Sonka']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Sonka']['Name'], data.Product['Sonka']['Quantity'], data.Product['Sonka']['NetPrice'],
                                       module=True)

        self.productseed.createProduct(data.Product['Paradicsomszósz']['Name'],
                                       data.Product['Paradicsomszósz']['ProductGroup'],
                                       data.Product['Paradicsomszósz']['Code'], data.Counter['TestCounter']['Name'],
                                       data.RawMaterial['Paradicsomszósz']['Name'], data.Product['Paradicsomszósz']['Quantity'], '0',
                                       module=True)


        # self.menu.openRestaurant()
        # self.html.clickElement(data.Table['Normal']['Name'], tag='i')


        self.address = self.clientseed.createRegular(self.name, self.code, self.phone, self.discount, self.taxnumber,
                                                self.country, self.postalCode, self.city,
                                                self.street, self.housenumber, module=True)



        self.menu.openProducts()

    @classmethod
    def tearDownClass(self):
        self.restaurantseed.deleteTable(data.Table['Normal']['Name'], module=True)
        self.restaurantseed.deleteTable(data.Table['Courier']['Name'], module=True)
        super().tearDownClass()

    def tearDown(self):

        self.productseed.deleteProduct(data.Product['Hasábburgonya']['Name'], module=True)
        self.productseed.deleteProduct('Roston csirkemell') #TODO Ezt itt ki kell pakolni
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

        self.clientseed.deleteRegular(self.name, module=True)

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

    # modositottam h adjon mennyiseget is hozza (BA)
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
        #self.html.fillInput('Termék mennyiségi tartalma', '100')
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
        self.createProductAsRawMaterial() # cola

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
        self.html.wait(2)
        self.html.refresh()

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



    def testPartPrice(self):
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

        for i in range(10):
            self.addProductToList('Rántott csirkemell', '1.00')
            self.html.wait(3)

        self.html.clickElement('Rendelés beküldése', waitSeconds=3)

        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
        self.html.clickElement('Fizetendő részösszeg')
        self.html.fillInput('Részösszeg','10000')
        self.html.getElements(None, '//button[contains(.,"OK")]', Options(uniqueSelector='True'))[1].click()
        self.html.wait(2)
        self.html.clickElement('Kijelöltek fizetése')

        price = self.html.getElement('Összesen', 'h2', Options(following='span')).text.split('.')[0]
        print(price)


        self.html.clickElement('Készpénz', 'td', Options(following='button'))

        self.html.clickElement('payDialogButton', 'button', Options(htmlAttribute='id'))
        stvalue = startValue.split(' ')
        prc = price.split(' ')
        prcInt = int(prc[0] + prc[1])
        self.assertGreaterEqual(prcInt,10000)
        print('prcInt:')
        print(prcInt)
        expected = int(stvalue[0] + stvalue[1]) + prcInt
        self.menu.openFinance()
        self.html.refresh()
        self.html.wait()
        actual = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2].split(' ')
        actInt = int(actual[0] + actual[1])

        self.assertEqual(expected, actInt)


    def testReceiving(self):
        self.receivingseed.createPartner(data.Partner['Szallito']['Name'], data.Partner['Szallito']['Name'], module=True)
        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()
        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)
        self.menu.openReceiving()
        self.html.clickElement('Új bevételezés', 'a', waitSeconds=2)
        # self.html.clickElement('Új')
        self.html.switchFrame('iframe')

        self.html.fillInput('Számla azonosító', 'KomplexTest')
        self.html.clickDropdown('Fizetési mód', 'Készpénz')
        self.html.clickDropdown('Beszállító', data.Partner['Szallito']['Name'])


        self.html.fillAutocomplete('Nyersanyag neve', 'input', data.RawMaterial['Csirkemell']['Name'],  data.RawMaterial['Csirkemell']['Name'], 'li', Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '1000', 'data-title')
        self.html.clickElement('Válassz...')
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.fillAutocomplete('Nyersanyag neve', 'input', data.RawMaterial['Finomliszt']['Name'],
                                   data.RawMaterial['Finomliszt']['Name'], 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '150', 'data-title')
        self.html.clickElement('Válassz...')
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.fillAutocomplete('Nyersanyag neve', 'input', data.RawMaterial['Almalé']['Name'],
                                   data.RawMaterial['Almalé']['Name'], 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '300', 'data-title')
        self.html.clickElement('Válassz...')
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.fillAutocomplete('Nyersanyag neve', 'input', data.RawMaterial['Hasábburgonya']['Name'],
                                   data.RawMaterial['Hasábburgonya']['Name'], 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '200', 'data-title')
        self.html.clickElement('Válassz...')
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.fillAutocomplete('Nyersanyag neve', 'input', data.RawMaterial['Sonka']['Name'],
                                   data.RawMaterial['Sonka']['Name'], 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '1800', 'data-title')
        self.html.clickElement('Válassz...')
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.fillAutocomplete('Nyersanyag neve', 'input', data.RawMaterial['Paradicsomszósz']['Name'],
                                   data.RawMaterial['Paradicsomszósz']['Name'], 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '2000', 'data-title')
        self.html.clickElement('Válassz...')
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.fillAutocomplete('Nyersanyag neve', 'input', 'Kóla', 'Kóla', 'li', Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '200', 'data-title')
        self.html.clickElement('Válassz...')
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)


        self.html.clickElement('Rögzít')

        self.html.switchFrame()

        self.stockAssert.assertStock(data.RawMaterial['Csirkemell']['Name'],data.WareHouses['Szeszraktár']['Name'], '20')
        self.html.wait(2)

        self.stockAssert.assertStock(data.RawMaterial['Finomliszt']['Name'], data.WareHouses['Szeszraktár']['Name'], '20')
        self.html.wait(2)

        self.stockAssert.assertStock(data.RawMaterial['Almalé']['Name'], data.WareHouses['Szeszraktár']['Name'], '20')
        self.html.wait(2)

        self.stockAssert.assertStock(data.RawMaterial['Hasábburgonya']['Name'], data.WareHouses['Szeszraktár']['Name'], '20')
        self.html.wait(2)

        self.stockAssert.assertStock(data.RawMaterial['Sonka']['Name'], data.WareHouses['Szeszraktár']['Name'], '20')
        self.html.wait(2)

        self.stockAssert.assertStock(data.RawMaterial['Paradicsomszósz']['Name'], data.WareHouses['Szeszraktár']['Name'], '20')
        self.html.wait(2)

        self.stockAssert.assertStock('Kóla', data.WareHouses['Szeszraktár']['Name'], '10')
        self.html.wait(2)

        self.receivingseed.deleteParter(data.Partner['Szallito']['Name'], module=True)




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


    #@unittest.skip
    def testDynamic1(self):

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
        self.createProductAsRawMaterial() # cola

        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openRestaurant()
        self.html.clickElement('Dinamikus futár asztalok', 'a')
        self.restaurantseed.createDynamicCourierTable(self.name)
        self.html.wait(5)

        self.html.clickElement('Pizza (testreszabható)', 'a')
        self.html.wait(1)
        self.html.clickElement('Sonkás pizza', 'span')
        self.html.wait(1)

        self.html.refresh()
        self.addProductToList('Rántott csirkemell', '1.00')

        self.html.clickElement('Ital', 'a')
        self.html.wait(2)
        self.html.clickElement('Üdítők', 'a')
        self.html.wait(2)
        ''' -----------------------------------------------------------------  Kólával nem működik ---------------------'''
        # self.html.clickElement('Kóla', 'span')
        self.html.clickElement('Gyömbér', 'span')
        self.html.wait(2)

        self.addProductToList('Roston csirkemell', '1.00')
        self.html.wait(2)
        self.html.wait(2)

        self.menu.openRestaurant()
        self.html.clickElement('Dinamikus futár asztalok', 'a')
        self.html.clickElement('Pista ' + self.city + ' ' + self.street, 'a')

        self.html.wait(2)
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)

        self.html.clickElement('Dinamikus futár asztalok', 'a')
        self.html.clickElement('Pista ' + self.city + ' ' + self.street, 'a')
        self.html.clickElement('Fizetés')

        #self.html.getElement('sum', 'span', Options(htmlAttribute='class'))
        price = self.html.getElement('Összesen', 'h2', Options(following='span')).text.split('.')[0]
        print(price)

        self.html.clickElement('Kitölt')

        self.html.clickElement('payDialogButton', 'button', Options(htmlAttribute='id'))
        stvalue = startValue.split(' ')
        prc = price.split(' ')
        prcInt = int(prc[0] + prc[1])
        expected = int(stvalue[0]+stvalue[1]) + prcInt
        print('ex ' + str(expected))
        self.menu.openFinance()
        self.html.refresh()
        self.html.wait()
        actual = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2].split(' ')
        actInt = int(actual[0] + actual[1])
        print('act ' + str(actInt))

        self.assertEqual(expected, actInt)

    # sztorno
    @unittest.skip
    def testOrderStorno(self):
        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()
        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)
        # mennyiseg ellenorzese
        self.menu.openReceiving()
        self.html.clickElement('Új bevételezés', 'a', waitSeconds=2)
        # self.html.clickElement('Új')
        self.html.switchFrame('iframe')

        self.html.fillInput('Számla azonosító', 'KomplexTest')
        self.html.clickDropdown('Fizetési mód', 'Készpénz')
        self.html.clickDropdown('Beszállító', data.Partner['Szallito']['Name'])

        self.html.fillAutocomplete('Nyersanyag neve', 'input', 'Kóla', 'Kóla', 'li',
                                   Options(htmlAttribute='data-title'))
        self.html.fillInput('Mennyiség', '10', 'data-title')
        self.html.fillInput('Bruttó egységár (Ft)', '200', 'data-title')
        self.html.clickElement('Válassz...')
        self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
        self.html.clickElement('Hozzáad')
        self.html.wait(2)

        self.html.clickElement('Rögzít')

        self.html.switchFrame()

        self.stockAssert.assertStock('Kóla', data.WareHouses['Szeszraktár']['Name'], '10')
        self.html.wait(2)

        # vissza az etterembe
        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        self.addProductToList('Kóla', '1.00')
        self.html.refresh()
        self.html.clickElement('Rendelés beküldése', waitSeconds=3)
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        name = self.html.getTxtFromListTable2('2', '3')
        qty = self.html.getTxtFromListTable2('2', '5')
        storno = self.html.getTxtFromListTable2('2', '8')

        self.assertEqual(name.text, 'Kóla')
        self.assertEqual(qty.text, '1.00')
        self.assertEqual(storno.text, 'Sztornó')

        self.stockAssert.assertStock('Kóla', data.WareHouses['Szeszraktár']['Name'], '8')

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

        # johet a sztorno
        self.html.clickTableElement('tasks-list products ui-sortable', 'class', 'Kóla', 'div', 'Sztornó')
        self.html.clickElement('Vendég visszamondta (raktárba visszatesz)', waitSeconds=2)
        self.restaurantAssert.assertProductNotInList()
        self.restaurantAssert.assertStornoSucces('Kóla')

        self.stockAssert.assertStock('Kóla', data.WareHouses['Szeszraktár']['Name'], '10')
        self.receivingseed.deleteParter(data.Partner['Szallito']['Name'], module=True)

    '''_______________________________________________________WORKS__________________________________________________'''
    # athelyezes reszasztalra
    def testMove(self):
        inputName = data.Product['Sonka']['Name']

        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()  # cola

        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

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

    '''_______________________________________________________WORKS__________________________________________________'''
    # athelyezes masik asztalra
    def testMoveToTable(self):

        inputName = data.Product['Sonka']['Name']
        inputName2 = data.Product['Paradicsomszósz']['Name']

        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()  # cola

        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

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

    '''_______________________________________________________WORKS__________________________________________________'''
    # athelyezes foglalt asztalra
    def testMoveToReservedTable(self):
        inputName = data.Product['Sonka']['Name']
        inputName2 = data.Product['Paradicsomszósz']['Name']

        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()  # cola

        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

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

    '''_______________________________________________________WORKS__________________________________________________'''
    # bontas
    def testUnfold(self):
        self.html.wait(10)
        inputName = data.Product['Sonka']['Name']

        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()  # cola

        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')
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

    '''_______________________________________________________WORKS__________________________________________________'''
    def testUnion(self):
        inputName = data.Product['Sonka']['Name']

        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()  # cola

        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

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

    '''_______________________________________________________WORKS__________________________________________________'''
    def testUnionAll(self):
        inputName = data.Product['Sonka']['Name']
        inputName2 = data.Product['Paradicsomszósz']['Name']

        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()  # cola

        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openRestaurant()
        self.html.clickElement(data.Table['Normal']['Name'], tag='i')

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

    '''_______________________________________________________WORKS__________________________________________________'''
    def testCreateCardDrink(self):
        name = data.DiscountCard['White Friday']['Name']
        code = data.DiscountCard['White Friday']['Code']
        discount = data.DiscountCard['White Friday']['Discount']
        category = data.DiscountCard['White Friday']['Category']

        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()  # cola

        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openClientManagement()
        self.html.clickElement('Kedvezménykártyák', 'a')

        self.html.clickElement('Új kedvezménykártya', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Megnevezés', name)
        self.html.fillInput('Kód', code)

        self.html.clickDropdown('Kategóriák', category)
        self.html.clickElement('Kategóriák', 'label')
        self.html.clickElement('dc_is_percent', 'label', options=Options(htmlAttribute='data-name'))

        for day in self.days:
            self.html.fillInput(day, discount, 'input', options=Options(htmlAttribute='data-title'))

        self.html.clickElement('Rögzít')

        self.clientAssert.assertDiscountCardExist(name, code, discount, category='Ital')
        self.clientseed.deleteCard(data.DiscountCard['White Friday']['Name'])

    '''_______________________________________________________WORKS__________________________________________________'''
    def testCreateCardFood(self):
        name = data.DiscountCard['Blue Friday']['Name']
        code = data.DiscountCard['Blue Friday']['Code']
        discount = data.DiscountCard['Blue Friday']['Discount']
        category = data.DiscountCard['Blue Friday']['Category']

        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()  # cola
        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openClientManagement()
        self.html.clickElement('Kedvezménykártyák', 'a')

        self.html.clickElement('Új kedvezménykártya', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Megnevezés', name)
        self.html.fillInput('Kód', code)

        self.html.clickDropdown('Kategóriák', category)
        self.html.clickElement('Kategóriák', 'label')
        self.html.clickElement('dc_is_percent', 'label', options=Options(htmlAttribute='data-name'))

        for day in self.days:
            self.html.fillInput(day, discount, 'input', options=Options(htmlAttribute='data-title'))

        self.html.clickElement('Rögzít')

        self.clientAssert.assertDiscountCardExist(name, code, discount, category='Étel')
        self.clientseed.deleteCard(data.DiscountCard['Blue Friday']['Name'])

    '''_______________________________________________________WORKS__________________________________________________'''
    def testCreateCardAll(self):
        name = data.DiscountCard['Blue Friday']['Name']
        code = data.DiscountCard['Blue Friday']['Code']
        discount = data.DiscountCard['Blue Friday']['Discount']
        category = data.DiscountCard['Blue Friday']['Category']

        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()  # cola
        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openClientManagement()
        self.html.clickElement('Kedvezménykártyák', 'a')

        self.html.clickElement('Új kedvezménykártya', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Megnevezés', name)
        self.html.fillInput('Kód', code)

        self.html.getElement('Kategóriák', 'label', Options(following='button')).click()
        self.html.clickElement('Mind', 'a')
        #self.html.clickDropdown('Kategóriák', category)
        self.html.clickElement('Kategóriák', 'label')
        self.html.clickElement('dc_is_percent', 'label', options=Options(htmlAttribute='data-name'))

        for day in self.days:
            self.html.fillInput(day, discount, 'input', options=Options(htmlAttribute='data-title'))

        self.html.clickElement('Rögzít')

        self.clientAssert.assertDiscountCardExist(name, code, discount, category='all')
        self.clientseed.deleteCard(data.DiscountCard['Blue Friday']['Name'])

    '''_______________________________________________________WORKS__________________________________________________'''
    def testCreateCardGroup(self):
        name = data.DiscountCard['White Friday']['Name']
        code = data.DiscountCard['White Friday']['Code']
        discount = data.DiscountCard['White Friday']['Discount']
        category = data.DiscountCard['White Friday']['Category']
        productGroup = data.DiscountCard['White Friday']['ProductGroup']

        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()  # cola
        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openClientManagement()
        self.html.clickElement('Kedvezménykártyák', 'a')

        self.html.clickElement('Új kedvezménykártya', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Megnevezés', name)
        self.html.fillInput('Kód', code)

        self.html.clickDropdown('Kategóriák', category)
        self.html.clickElement('Kategóriák', 'label')
        self.html.clickElement('Termékcsoportok', 'label', options=Options(following='input'))
        self.html.switchFrame('iframe')
        self.html.clickElement(productGroup, 'a')
        self.html.clickElement('Rögzít')
        self.html.switchFrame('iframe')
        self.html.clickElement('dc_is_percent', 'label', options=Options(htmlAttribute='data-name'))

        for day in self.days:
            self.html.fillInput(day, discount, 'input', options=Options(htmlAttribute='data-title'))

        self.html.clickElement('Rögzít')

        self.clientAssert.assertDiscountCardExist(name, code, discount, group=productGroup, category='Ital')
        self.clientseed.deleteCard(data.DiscountCard['White Friday']['Name'])

    '''_______________________________________________________WORKS__________________________________________________'''
    def testCreateCardProduct(self):
        name = data.DiscountCard['White Friday']['Name']
        code = data.DiscountCard['White Friday']['Code']
        discount = data.DiscountCard['White Friday']['Discount']
        category = data.DiscountCard['White Friday']['Category']
        productGroup = data.DiscountCard['White Friday']['ProductGroup']
        product = data.DiscountCard['White Friday']['Product']

        self.menu.openProducts()
        self.createProductChose()
        self.menu.openProducts()
        self.createProductFix()
        self.createProductAsRawMaterial()  # cola
        self.createPizza('Sonkás pizza', data.RawMaterial['Finomliszt']['Name'], data.Product['Sonka']['Name'],
                         module=True)

        self.menu.openClientManagement()
        self.html.clickElement('Kedvezménykártyák', 'a')

        self.html.clickElement('Új kedvezménykártya', 'a')
        self.html.switchFrame('iframe')

        self.html.fillInput('Megnevezés', name)
        self.html.fillInput('Kód', code)

        self.html.clickDropdown('Kategóriák', category)
        self.html.clickElement('Kategóriák', 'label')
        self.html.clickElement('Termékcsoportok', 'label', options=Options(following='input'))
        self.html.switchFrame('iframe')
        self.html.clickElement(productGroup, 'a')
        self.html.clickElement('Rögzít')
        self.html.switchFrame('iframe')
        self.html.clickDropdown('Termékek', product) # itt majd lehet egy keresest be kell epiteni
        self.html.clickElement('Termékek', 'label')
        self.html.clickElement('dc_is_percent', 'label', options=Options(htmlAttribute='data-name'))

        for day in self.days:
            self.html.fillInput(day, discount, 'input', options=Options(htmlAttribute='data-title'))

        self.html.clickElement('Rögzít')

        self.clientAssert.assertDiscountCardExist(name, code, discount, group=productGroup, category='Ital', products=product)
        self.clientseed.deleteCard(data.DiscountCard['White Friday']['Name'])

    @unittest.skip
    def testCreateRegular(self):
        self.clientAssert.assertRegularExist(self.name, self.address, self.phone,
                                            self.discount, self.code)

        self.clientseed.deleteRegular(self.name)

