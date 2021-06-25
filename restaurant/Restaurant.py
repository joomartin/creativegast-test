''' Na ez hosszu menet lesz...'''
import unittest

from selenium.webdriver.support.wait import WebDriverWait

from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class Restaurant(BaseTestCase):
    rawMaterials = ['Csirkemell', 'Finomliszt', 'Almalé', 'Hasábburgonya', 'Sonka', 'Paradicsomszósz']

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
    address = city + ' ' + street + ' ' + housenumber

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
                                       '9999', data.Counter['TestCounter']['Name'], data.RawMaterial['Almalé']['Name'],
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
        try:
            self.receivingseed.deleteParter(data.Partner['Szallito']['Name'], module=True)
        except Exception:
            pass
        try:
            self.restaurantseed.deleteTable('Kedvezmeny', module=True)
        except Exception:
            pass
        try:
            self.restaurantseed.deleteTable('Elvitel', module=True)
        except Exception:
            pass
        try:
            self.productseed.deleteProduct(data.Product['Babgulyás']['Name'], module=True)
        except Exception:
            pass
        try:
            self.productseed.deleteProduct(data.Product['Palacsinta']['Name'], module=True)
        except Exception:
            pass
        try:
            self.productseed.deleteCounter(data.Counter['TestCounter']['Name'], tab=True)
        except Exception:
            pass
        try:
            self.productseed.deleteProduct(data.Product['Hasábburgonya']['Name'], module=True)
        except Exception:
            pass
        try:
            self.productseed.deleteProduct('Roston csirkemell', module=True)
        except Exception:
            pass
        try:
            self.productseed.deleteProduct('Rántott csirkemell', module=True)
        except Exception:
            pass
        try:
            self.productseed.deleteProduct('Almalé', module=True)
        except Exception:
            pass
        try:
            self.productseed.deleteProduct('Kóla', module=True)
        except Exception:
            pass
        try:
            self.productseed.deleteProduct(data.Product['Sonka']['Name'], module=True)
        except Exception:
            pass
        try:
            self.productseed.deleteProduct(data.Product['Paradicsomszósz']['Name'], module=True)
        except Exception:
            pass
        try:
            self.productseed.deletePizza('Sonkás pizza', module=True)
        except Exception:
            pass
        try:
            self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True)
        except Exception:
            pass
        try:
            self.stockseed.deleteRawMaterial(data.RawMaterial['Alma']['Name'], module=True)
        except Exception:
            pass
        try:
            self.stockseed.deleteRawMaterial('Kóla', module=True)
        except Exception:
            pass
        for material in self.rawMaterials:
            try:
                self.stockseed.deleteRawMaterial(data.RawMaterial[material]['Name'], module=True)
            except Exception:
                pass
        try:
            self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True)
        except Exception:
            pass
        '''
        self.tryHelper(self.receivingseed.deleteParter(data.Partner['Szallito']['Name'], module=True))
        self.tryHelper(self.restaurantseed.deleteTable('Kedvezmeny', module=True))
        self.tryHelper(self.restaurantseed.deleteTable('Elvitel', module=True))
        self.tryHelper(self.productseed.deleteProduct(data.Product['Babgulyás']['Name'], module=True))
        self.tryHelper(self.productseed.deleteProduct(data.Product['Palacsinta']['Name'], module=True))
        self.tryHelper(self.productseed.deleteCounter(data.Counter['TestCounter']['Name'], tab=True))
        self.tryHelper(self.productseed.deleteProduct(data.Product['Hasábburgonya']['Name'], module=True))
        self.tryHelper(self.productseed.deleteProduct('Roston csirkemell', module=True))
        self.tryHelper(self.productseed.deleteProduct('Rántott csirkemell', module=True))
        self.tryHelper(self.productseed.deleteProduct('Almalé', module=True))
        self.tryHelper(self.productseed.deleteProduct('Kóla', module=True))
        self.tryHelper(self.productseed.deleteProduct(data.Product['Sonka']['Name'], module=True))
        self.tryHelper(self.productseed.deleteProduct(data.Product['Paradicsomszósz']['Name'], module=True))
        self.tryHelper(self.productseed.deletePizza('Sonkás pizza', module=True))
        self.tryHelper(self.stockseed.deleteRawMaterial(data.RawMaterial['Bundas_kenyer']['Name'], module=True))
        self.tryHelper(self.stockseed.deleteRawMaterial(data.RawMaterial['Alma']['Name'], module=True))
        self.tryHelper(self.stockseed.deleteRawMaterial('Kóla', module=True))
        for material in self.rawMaterials:
            self.tryHelper(self.stockseed.deleteRawMaterial(data.RawMaterial[material]['Name'], module=True))
        self.tryHelper(self.stockseed.deleteWarehouse(data.WareHouses['Szeszraktár']['Name'], tab=True))
        '''

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









    # passed
    ##@unittest.skip
    def testMultipleOrders(self):
        def wrapper():
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
            self.html.wait(5)
            self.menu.openFinance()
            self.html.refresh()
            self.html.wait()
            actual = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2].split(' ')
            actInt = int(actual[0] + actual[1])

            self.assertEqual(expected, actInt)

        super(Restaurant, self).runTest(wrapper, 'restaurant-testMultipleOrders')

    # passed
    #@unittest.skip
    def testMultipleOrdersCredit(self):
        def wrapper():
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
            self.html.wait(5)
            self.menu.openFinance()
            self.html.refresh()
            self.html.wait()
            actual = self.html.getElement('Bankkártya', 'td', Options(following='td')).text[:-2].split(' ')
            actInt = int(actual[0] + actual[1])

            self.assertEqual(expected, actInt)
            #self.html.switchFrame('iframe')

        super(Restaurant, self).runTest(wrapper, 'restaurant-testMultipleOrdersCredit')

    # passed
    #@unittest.skip
    def testInstantPayment(self):
        def wrapper():
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
            self.html.wait(5)
            self.menu.openFinance()
            self.html.refresh()
            self.html.wait()
            actual = self.html.getElement('Bankkártya', 'td', Options(following='td')).text[:-2].split(' ')
            actInt = int(actual[0] + actual[1])

            self.assertEqual(expected, actInt)

        super(Restaurant, self).runTest(wrapper, 'restaurant-testInstantPayment')

    # passed
    #@unittest.skip
    def testDiscountedTable(self):
        def wrapper():
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
            self.html.wait(5)
            self.menu.openFinance()
            self.html.refresh()
            self.html.wait()
            actual = self.html.getElement('Bankkártya', 'td', Options(following='td')).text[:-2].split(' ')
            actInt = int(actual[0] + actual[1])

            self.assertEqual(expected, actInt)

            # self.restaurantseed.deleteTable('Kedvezmeny', module=True)

        super(Restaurant, self).runTest(wrapper, 'restaurant-testDiscountedTable')

    # passed
    #@unittest.skip
    def testTake(self):
        def wrapper():
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
            self.html.wait(10)
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

        super(Restaurant, self).runTest(wrapper, 'restaurant-testTake')

    # passed
    #@unittest.skip
    def testPartPrice(self):
        def wrapper():
            self.menu.openFinance()
            try:
                startValue = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2]
            except:
                startValue = '0 0'

            self.menu.openRestaurant()

            self.html.clickElement(data.Table['Normal']['Name'], tag='i')

            for i in range(10):
                self.addProductToList('Rántott csirkemell', '1.00')
                self.html.wait(3)

            self.html.clickElement('Rendelés beküldése', waitSeconds=3)

            self.html.clickElement(data.Table['Normal']['Name'], tag='i')
            self.html.clickElement('Fizetendő részösszeg')
            self.html.fillInput('Részösszeg', '12000')
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
            self.assertGreaterEqual(prcInt, 10000)
            print('prcInt:')
            print(prcInt)
            expected = int(stvalue[0] + stvalue[1]) + prcInt
            print('startValue:')
            print(stvalue)
            print('expected:')
            print(expected)
            self.html.wait(5)
            self.menu.openFinance()
            self.html.refresh()
            self.html.wait()
            actual = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2].split(' ')
            actInt = int(actual[0] + actual[1])
            print()
            print(actual)
            print(actInt)

            # maradekok eltuntetese
            self.menu.openRestaurant()
            self.html.clickElement(data.Table['Normal']['Name'], tag='i')
            self.html.clickElement('Fizetés')
            self.html.clickElement('Kitölt')
            self.html.clickElement('payDialogButton', 'button', Options(htmlAttribute='id'))

            self.assertEqual(expected, actInt)

        super(Restaurant, self).runTest(wrapper, 'restaurant-testPartPrice')

    # passed
    #@unittest.skip
    def testDynamic1(self):
        def wrapper():
            self.menu.openFinance()
            try:
                startValue = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2]
            except:
                startValue = '0 0'
            print(startValue)

            self.receivingseed.createPartner(data.Partner['Szallito']['Name'], data.Partner['Szallito']['Name'], module=True)
            self.clientseed.createClient(self.name, self.code, self.phone, self.discount, self.taxnumber, self.country,
                                         self.postalCode, self.city, self.street, self.housenumber, module=True)

            # mennyiseg ellenorzese
            self.menu.openReceiving()
            self.html.clickElement('Új bevételezés', 'a', waitSeconds=2)
            try:
                self.html.clickElement('Új')
            except Exception:
                pass
            self.html.switchFrame('iframe')

            self.html.fillInput('Számla azonosító', 'KomplexTest')
            self.html.clickDropdown('Fizetési mód', 'Készpénz')
            self.html.clickDropdown('Beszállító', data.Partner['Szallito']['Name'])

            self.html.fillAutocomplete('Nyersanyag neve', 'input', 'Kóla', 'Kóla', 'li',
                                       Options(htmlAttribute='data-title'))
            self.html.fillInput('Mennyiség', '10', 'data-title')
            self.html.fillInput('Bruttó egységár (Ft)', '200', 'data-title')
            self.html.clickElement('Válassz...')
            firstrow = self.html.getElement('firstrow', 'tr', options=Options(htmlAttribute='class'))
            warehouse = self.html.getElements('search', 'div', options=Options(htmlAttribute='class', element=firstrow))
            #self.html.wait(2)
            wait = WebDriverWait(self.driver, 5000)
            wait.until(ec.element_to_be_clickable(
                (By.XPATH, '//*[@id="dialogtabs-base"]/div/div[2]/table/tbody/tr/td[6]/div/div/div/input')))
            self.html.fillInput('Keresett kifejezés', data.WareHouses['Szeszraktár']['Name'], 'input',
                                options=Options(htmlAttribute='placeholder', element=warehouse[2]))
            self.html.wait(2)
            self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
            self.html.clickElement('Hozzáad')
            self.html.wait(2)

            self.html.clickElement('Rögzít')

            self.html.switchFrame()

            self.stockAssert.assertStock('Kóla', data.WareHouses['Szeszraktár']['Name'], '10')
            self.html.wait(2)

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
            self.html.clickElement('Kóla', 'span', options=Options(exactMatch=True))
            #self.html.clickElement('Gyömbér', 'span')
            self.html.wait(2)

            self.addProductToList('Roston csirkemell', '1.00')
            self.html.wait(4)

            self.menu.openRestaurant()
            self.html.clickElement('Dinamikus futár asztalok', 'a')
            self.html.clickElement(self.name + ' ' + self.city + ' ' + self.street, 'a')

            self.html.wait(2)
            self.html.clickElement('Rendelés beküldése', waitSeconds=3)

            self.html.clickElement('Dinamikus futár asztalok', 'a')
            self.html.clickElement(self.name + ' ' + self.city + ' ' + self.street, 'a')
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
            self.html.wait(5)
            self.menu.openFinance()
            self.html.refresh()
            self.html.wait()
            actual = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2].split(' ')
            actInt = int(actual[0] + actual[1])
            print('act ' + str(actInt))

            self.assertEqual(expected, actInt)

        super(Restaurant, self).runTest(wrapper, 'restaurant-testDynamic1')

    # passed
    ##@unittest.skip
    def testOrderStorno(self):
        def wrapper():
            self.receivingseed.createPartner(data.Partner['Szallito']['Name'], data.Partner['Szallito']['Name'], module=True)

            # mennyiseg ellenorzese
            self.menu.openReceiving()
            self.html.clickElement('Új bevételezés', 'a', waitSeconds=2)
            try:
                self.html.clickElement('Új')
            except Exception:
                pass
            self.html.switchFrame('iframe')

            self.html.fillInput('Számla azonosító', 'KomplexTest')
            self.html.clickDropdown('Fizetési mód', 'Készpénz')
            self.html.clickDropdown('Beszállító', data.Partner['Szallito']['Name'])

            self.html.fillAutocomplete('Nyersanyag neve', 'input', 'Kóla', 'Kóla', 'li',
                                       Options(htmlAttribute='data-title'))
            self.html.fillInput('Mennyiség', '10', 'data-title')
            self.html.fillInput('Bruttó egységár (Ft)', '200', 'data-title')
            self.html.clickElement('Válassz...')
            firstrow = self.html.getElement('firstrow', 'tr', options=Options(htmlAttribute='class'))
            warehouse = self.html.getElements('search', 'div', options=Options(htmlAttribute='class', element=firstrow))
            #self.html.wait(2)
            wait = WebDriverWait(self.driver, 5000)
            wait.until(ec.element_to_be_clickable(
                (By.XPATH, '//*[@id="dialogtabs-base"]/div/div[2]/table/tbody/tr/td[6]/div/div/div/input')))
            self.html.fillInput('Keresett kifejezés', data.WareHouses['Szeszraktár']['Name'], 'input',
                                options=Options(htmlAttribute='placeholder', element=warehouse[2]))
            self.html.wait(2)
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

            self.stockAssert.assertStock('Kóla', data.WareHouses['Szeszraktár']['Name'], '9')

            self.menu.openRestaurant()
            self.html.clickElement(data.Table['Normal']['Name'], tag='i')

            # johet a sztorno
            self.html.clickTableElement('tasks-list products ui-sortable', 'class', 'Kóla', 'div', 'Sztornó')
            self.html.clickElement('Vendég visszamondta (raktárba visszatesz)', waitSeconds=2)
            self.restaurantAssert.assertProductNotInList()
            self.restaurantAssert.assertStornoSucces('Kóla')

            self.stockAssert.assertStock('Kóla', data.WareHouses['Szeszraktár']['Name'], '10')
            #self.receivingseed.deleteParter(data.Partner['Szallito']['Name'], module=True)

        super(Restaurant, self).runTest(wrapper, 'restaurant-testOrderStorno')

    # passed
    #@unittest.skip
    def testWrongorderStorno(self):
        def wrapper():
            self.receivingseed.createPartner(data.Partner['Szallito']['Name'], data.Partner['Szallito']['Name'],
                                             module=True)
            # mennyiseg ellenorzese
            self.menu.openReceiving()
            self.html.clickElement('Új bevételezés', 'a', waitSeconds=2)
            try:
                self.html.clickElement('Új')
            except Exception:
                pass
            self.html.switchFrame('iframe')

            self.html.fillInput('Számla azonosító', 'KomplexTest')
            self.html.clickDropdown('Fizetési mód', 'Készpénz')
            self.html.clickDropdown('Beszállító', data.Partner['Szallito']['Name'])

            self.html.fillAutocomplete('Nyersanyag neve', 'input', 'Kóla', 'Kóla', 'li',
                                       Options(htmlAttribute='data-title'))
            self.html.fillInput('Mennyiség', '10', 'data-title')
            self.html.fillInput('Bruttó egységár (Ft)', '200', 'data-title')
            self.html.clickElement('Válassz...')
            firstrow = self.html.getElement('firstrow', 'tr', options=Options(htmlAttribute='class'))
            warehouse = self.html.getElements('search', 'div', options=Options(htmlAttribute='class', element=firstrow))
            #self.html.wait(2)
            wait = WebDriverWait(self.driver, 5000)
            wait.until(ec.element_to_be_clickable(
                (By.XPATH, '//*[@id="dialogtabs-base"]/div/div[2]/table/tbody/tr/td[6]/div/div/div/input')))
            self.html.fillInput('Keresett kifejezés', data.WareHouses['Szeszraktár']['Name'], 'input',
                                options=Options(htmlAttribute='placeholder', element=warehouse[2]))
            self.html.wait(2)
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

            # rendeles bekuldese
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

            # ez lehet itt nem kell, de nem baj ha van
            self.stockAssert.assertStock('Kóla', data.WareHouses['Szeszraktár']['Name'], '9')

            self.menu.openRestaurant()
            self.html.clickElement(data.Table['Normal']['Name'], tag='i')

            # johet a sztorno
            self.html.clickTableElement('tasks-list products ui-sortable', 'class', 'Kóla', 'div', 'Sztornó')
            self.html.clickElement('Hibás rendelés (raktárba visszatesz)', waitSeconds=4)

            self.restaurantAssert.assertProductNotInList()
            self.restaurantAssert.assertStornoSucces('Kóla')

            # mennyiseg ellenorzese
            self.stockAssert.assertStock('Kóla', data.WareHouses['Szeszraktár']['Name'], '10')
            #self.receivingseed.deleteParter(data.Partner['Szallito']['Name'], module=True)

        super(Restaurant, self).runTest(wrapper, 'restaurant-testWrongOrderStorno')

    # passed
    #@unittest.skip
    def testQualityStorno(self):
        def wrapper():
            self.receivingseed.createPartner(data.Partner['Szallito']['Name'], data.Partner['Szallito']['Name'],
                                             module=True)
            # mennyiseg ellenorzese
            self.menu.openReceiving()
            self.html.clickElement('Új bevételezés', 'a', waitSeconds=2)
            try:
                self.html.clickElement('Új')
            except Exception:
                pass
            self.html.switchFrame('iframe')

            self.html.fillInput('Számla azonosító', 'KomplexTest')
            self.html.clickDropdown('Fizetési mód', 'Készpénz')
            self.html.clickDropdown('Beszállító', data.Partner['Szallito']['Name'])

            self.html.fillAutocomplete('Nyersanyag neve', 'input', 'Kóla', 'Kóla', 'li',
                                       Options(htmlAttribute='data-title'))
            self.html.fillInput('Mennyiség', '10', 'data-title')
            self.html.fillInput('Bruttó egységár (Ft)', '200', 'data-title')
            self.html.clickElement('Válassz...')
            firstrow = self.html.getElement('firstrow', 'tr', options=Options(htmlAttribute='class'))
            warehouse = self.html.getElements('search', 'div', options=Options(htmlAttribute='class', element=firstrow))
            #self.html.wait(2)
            wait = WebDriverWait(self.driver, 5000)
            wait.until(ec.element_to_be_clickable(
                (By.XPATH, '//*[@id="dialogtabs-base"]/div/div[2]/table/tbody/tr/td[6]/div/div/div/input')))
            self.html.fillInput('Keresett kifejezés', data.WareHouses['Szeszraktár']['Name'], 'input',
                                options=Options(htmlAttribute='placeholder', element=warehouse[2]))
            self.html.wait(2)
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

            # rendeles bekuldese
            self.addProductToList('Kóla', '1.00')
            self.html.refresh()
            self.html.clickElement('Rendelés beküldése', waitSeconds=3)
            self.html.clickElement(data.Table['Normal']['Name'], tag='i')

            name = self.html.getTxtFromListTable2('2', '3')
            qty = self.html.getTxtFromListTable2('2', '5')
            storno = self.html.getTxtFromListTable2('2', '8')

            # csekkolas
            self.assertEqual(name.text, 'Kóla')
            self.assertEqual(qty.text, '1.00')
            self.assertEqual(storno.text, 'Sztornó')

            # ez lehet itt nem kell, de nem baj ha van
            self.stockAssert.assertStock('Kóla', data.WareHouses['Szeszraktár']['Name'], '9')

            self.menu.openRestaurant()
            self.html.clickElement(data.Table['Normal']['Name'], tag='i')

            # johet a sztorno
            self.html.clickTableElement('tasks-list products ui-sortable', 'class', 'Kóla', 'div', 'Sztornó')
            self.html.clickElement('Minőségi kifogás', waitSeconds=1)
            self.html.fillInput('Minőségi kifogás indoka', 'teszt01 sztornó', 'textarea', options=Options(htmlAttribute='placeholder'))
            self.html.clickElement('Minőségi kifogás küldése', waitSeconds=2)

            self.restaurantAssert.assertProductNotInList()
            self.restaurantAssert.assertStornoSucces('Kóla')

            # mennyiseg ellenorzese
            self.stockAssert.assertStock('Kóla', data.WareHouses['Szeszraktár']['Name'], '9')

            # selejt ellenorzese
            self.html.clickElement('Selejtezések', 'a')
            name = self.html.getElementInTable('Kóla', 'component_waste', 'Selejtezések').is_displayed()
            excuse = self.html.getTxtFromTable('1', '5', 'component_waste')
            self.assertTrue(name)
            self.assertEqual(excuse, 'teszt01 sztornó')

            #self.receivingseed.deleteParter(data.Partner['Szallito']['Name'], module=True)

        super(Restaurant, self).runTest(wrapper, 'restaurant-testQualityStorno')

    # passed
    #@unittest.skip
    def testMove(self):
        def wrapper():
            inputName = data.Product['Sonka']['Name']

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

        super(Restaurant, self).runTest(wrapper, 'restaurant-testMove')

    # passed
    ##@unittest.skip
    def testMoveToTable(self):
        def wrapper():
            inputName = data.Product['Sonka']['Name']
            inputName2 = data.Product['Paradicsomszósz']['Name']

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

        super(Restaurant, self).runTest(wrapper, 'restaurant-testMoveToTable')

    # passed
    #@unittest.skip
    def testMoveToReservedTable(self):
        def wrapper():
            inputName = data.Product['Sonka']['Name']
            inputName2 = data.Product['Paradicsomszósz']['Name']

            self.menu.openRestaurant()
            self.html.clickElement(data.Table['Normal']['Name'], tag='i')

            # elso asztalra rendeles bekuldese
            self.addProductToList(inputName, '1.00')
            self.html.refresh()
            self.html.wait(2)
            self.html.clickElement('Rendelés beküldése', waitSeconds=3)
            self.html.clickElement(data.Table['Courier']['Name'], tag='i')

            # masodik asztalra rendeles bekuldese
            self.addProductToList(inputName, '1.00')
            self.addProductToList(inputName2, '1.00')
            self.html.refresh()
            self.html.wait(2)
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

        super(Restaurant, self).runTest(wrapper, 'restaurant-testMoveToReservedTable')

    # passed
    #@unittest.skip
    def testUnfold(self):
        def wrapper():
            self.html.wait(10)
            inputName = data.Product['Sonka']['Name']

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

        super(Restaurant, self).runTest(wrapper, 'restaurant-testUnfold')

    # passed
    #@unittest.skip
    def testUnion(self):
        def wrapper():
            inputName = data.Product['Sonka']['Name']

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

        super(Restaurant, self).runTest(wrapper, 'restaurant-testUnion')

    # passed
    #@unittest.skip
    def testUnionAll(self):
        def wrapper():
            inputName = data.Product['Sonka']['Name']
            inputName2 = data.Product['Paradicsomszósz']['Name']

            self.menu.openRestaurant()
            self.html.clickElement(data.Table['Normal']['Name'], tag='i')

            self.addProductToList(inputName, '1.00')
            self.addProductToList(inputName, '1.00')
            self.addProductToList(inputName2, '1.00')
            self.addProductToList(inputName2, '1.00')

            self.html.wait(2)
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

        super(Restaurant, self).runTest(wrapper, 'restaurant-testUnionAll')

    # passed
    #@unittest.skip
    def testDynamic2(self):
        def wrapper():
            self.menu.openFinance()
            try:
                startValue = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2]
            except:
                startValue = '0 0'
            print(startValue)

            self.receivingseed.createPartner(data.Partner['Szallito']['Name'], data.Partner['Szallito']['Name'], module=True)

            # mennyiseg ellenorzese
            self.menu.openReceiving()
            self.html.clickElement('Új bevételezés', 'a', waitSeconds=2)
            try:
                self.html.clickElement('Új')
            except Exception:
                pass
            self.html.switchFrame('iframe')

            self.html.fillInput('Számla azonosító', 'KomplexTest')
            self.html.clickDropdown('Fizetési mód', 'Készpénz')
            self.html.clickDropdown('Beszállító', data.Partner['Szallito']['Name'])

            self.html.fillAutocomplete('Nyersanyag neve', 'input', 'Kóla', 'Kóla', 'li',
                                       Options(htmlAttribute='data-title'))
            self.html.fillInput('Mennyiség', '10', 'data-title')
            self.html.fillInput('Bruttó egységár (Ft)', '200', 'data-title')
            self.html.clickElement('Válassz...')
            firstrow = self.html.getElement('firstrow', 'tr', options=Options(htmlAttribute='class'))
            warehouse = self.html.getElements('search', 'div', options=Options(htmlAttribute='class', element=firstrow))
            #self.html.wait(2)
            wait = WebDriverWait(self.driver, 5000)
            wait.until(ec.element_to_be_clickable(
                (By.XPATH, '//*[@id="dialogtabs-base"]/div/div[2]/table/tbody/tr/td[6]/div/div/div/input')))
            self.html.fillInput('Keresett kifejezés', data.WareHouses['Szeszraktár']['Name'], 'input',
                                options=Options(htmlAttribute='placeholder', element=warehouse[2]))
            self.html.wait(2)
            self.html.clickElement(data.WareHouses['Szeszraktár']['Name'], 'label')
            self.html.clickElement('Hozzáad')
            self.html.wait(2)

            self.html.clickElement('Rögzít')

            self.html.switchFrame()

            self.stockAssert.assertStock('Kóla', data.WareHouses['Szeszraktár']['Name'], '10')
            self.html.wait(2)

            self.menu.openRestaurant()
            self.html.clickElement('Dinamikus futár asztalok', 'a')
            self.restaurantseed.createDynCTableForNew(self.name, self.city, self.street, self.housenumber, self.phone)
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

            self.html.clickElement('Kóla', 'span', options=Options(exactMatch=True))
            #self.html.clickElement('Gyömbér', 'span')
            self.html.wait(2)

            self.addProductToList('Roston csirkemell', '1.00')
            self.html.wait(2)
            self.html.wait(2)

            self.menu.openRestaurant()
            self.html.clickElement('Dinamikus futár asztalok', 'a')
            self.html.clickElement(self.name + ' ' + self.city + ' ' + self.street, 'a')

            self.html.wait(2)
            self.html.clickElement('Rendelés beküldése', waitSeconds=3)

            self.html.clickElement('Dinamikus futár asztalok', 'a')
            self.html.clickElement(self.name + ' ' + self.city + ' ' + self.street, 'a')
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
            self.html.wait(5)
            self.menu.openFinance()
            self.html.refresh()
            self.html.wait()
            actual = self.html.getElement('Készpénz', 'td', Options(following='td')).text[:-2].split(' ')
            actInt = int(actual[0] + actual[1])
            print('act ' + str(actInt))

            self.assertEqual(expected, actInt)
            self.clientAssert.assertClientExist(self.name, self.address, self.phone, self.discount, self.code, extended=False, module=True)
            #self.receivingseed.deleteParter(data.Partner['Szallito']['Name'], module=True)

        super(Restaurant, self).runTest(wrapper, 'restaurant-testDynamic2')




    def tryHelper(self, func):
        try:
            func
        except Exception:
            pass















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
