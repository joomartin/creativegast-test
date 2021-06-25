from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options


class DiscountCards(BaseTestCase):
    days = ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap']

    nameWhite = data.DiscountCard['White Friday']['Name']
    codeWhite = data.DiscountCard['White Friday']['Code']
    discountWhite = data.DiscountCard['White Friday']['Discount']
    categoryWhite = data.DiscountCard['White Friday']['Category']
    productGroupWhite = data.DiscountCard['White Friday']['ProductGroup']
    productWhite = data.DiscountCard['White Friday']['Product']

    nameBlue = data.DiscountCard['Blue Friday']['Name']
    codeBlue = data.DiscountCard['Blue Friday']['Code']
    discountBlue = data.DiscountCard['Blue Friday']['Discount']
    categoryBlue = data.DiscountCard['Blue Friday']['Category']


    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

    def setUp(self):
        self.productseed.createProductAsRawMaterial(module=True)
        self.menu.openClientManagement()
        self.html.clickElement('Kedvezménykártyák', 'a')

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def tearDown(self):
        try:
            self.productseed.deleteProduct('Kóla', module=True)
        except Exception:
            pass
        try:
            self.stockseed.deleteRawMaterial('Kóla', module=True)
        except Exception:
            pass
        try:
            self.clientseed.deleteCard(data.DiscountCard['White Friday']['Name'], module=True)
        except Exception:
            pass
        try:
            self.clientseed.deleteCard(data.DiscountCard['Blue Friday']['Name'], module=True)
        except Exception:
            pass
        try:
            self.clientseed.deleteCard(data.DiscountCard['Blue Friday']['Name'], module=True)
        except Exception:
            pass
        try:
            self.clientseed.deleteCard(data.DiscountCard['White Friday']['Name'], module=True)
        except Exception:
            pass
        try:
            self.clientseed.deleteCard(data.DiscountCard['White Friday']['Name'], module=True)
        except Exception:
            pass

    def testCreateCardDrink(self):
        def wrapper():
            self.html.clickElement('Új kedvezménykártya', 'a')
            self.html.switchFrame('iframe')

            self.html.fillInput('Megnevezés', self.nameWhite)
            self.html.fillInput('Kód', self.codeWhite)

            self.html.clickDropdown('Kategóriák', self.categoryWhite)
            self.html.clickElement('Kategóriák', 'label')
            self.html.clickElement('dc_is_percent', 'label', options=Options(htmlAttribute='data-name'))

            for day in self.days:
                self.html.fillInput(day, self.discountWhite, 'input', options=Options(htmlAttribute='data-title'))

            self.html.clickElement('Rögzít')

            self.clientAssert.assertDiscountCardExist(self.nameWhite, self.codeWhite, self.discountWhite, category='Ital')
            # self.clientseed.deleteCard(data.DiscountCard['White Friday']['Name'])

        super(DiscountCards, self).runTest(wrapper, 'discountCards-testCreateCardDrink')

    def testCreateCardFood(self):
        def wrapper():
            self.html.clickElement('Új kedvezménykártya', 'a')
            self.html.switchFrame('iframe')

            self.html.fillInput('Megnevezés', self.nameBlue)
            self.html.fillInput('Kód', self.codeBlue)

            self.html.clickDropdown('Kategóriák', self.categoryBlue)
            self.html.clickElement('Kategóriák', 'label')
            self.html.clickElement('dc_is_percent', 'label', options=Options(htmlAttribute='data-name'))

            for day in self.days:
                self.html.fillInput(day, self.discountBlue, 'input', options=Options(htmlAttribute='data-title'))

            self.html.clickElement('Rögzít')

            self.clientAssert.assertDiscountCardExist(self.nameBlue, self.codeBlue, self.discountBlue, category='Étel')
            # self.clientseed.deleteCard(data.DiscountCard['Blue Friday']['Name'])

        super(DiscountCards, self).runTest(wrapper, 'discountCards-testCreateCardFood')

    def testCreateCardAll(self):
        def wrapper():
            self.html.clickElement('Új kedvezménykártya', 'a')
            self.html.switchFrame('iframe')

            self.html.fillInput('Megnevezés', self.nameBlue)
            self.html.fillInput('Kód', self.codeBlue)

            self.html.getElement('Kategóriák', 'label', Options(following='button')).click()
            self.html.clickElement('Mind', 'a')
            #self.html.clickDropdown('Kategóriák', category)
            self.html.clickElement('Kategóriák', 'label')
            self.html.clickElement('dc_is_percent', 'label', options=Options(htmlAttribute='data-name'))

            for day in self.days:
                self.html.fillInput(day, self.discountBlue, 'input', options=Options(htmlAttribute='data-title'))

            self.html.clickElement('Rögzít')

            self.clientAssert.assertDiscountCardExist(self.nameBlue, self.codeBlue, self.discountBlue, category='all')
            # self.clientseed.deleteCard(data.DiscountCard['Blue Friday']['Name'])

        super(DiscountCards, self).runTest(wrapper, 'discountCards-testCreateCardAll')

    def testCreateCardGroup(self):
        def wrapper():
            self.html.clickElement('Új kedvezménykártya', 'a')
            self.html.switchFrame('iframe')

            self.html.fillInput('Megnevezés', self.nameWhite)
            self.html.fillInput('Kód', self.codeWhite)

            self.html.clickDropdown('Kategóriák', self.categoryWhite)
            self.html.clickElement('Kategóriák', 'label')
            self.html.clickElement('Termékcsoportok', 'label', options=Options(following='input'))
            self.html.switchFrame('iframe')
            self.html.clickElement(self.productGroupWhite, 'a')
            self.html.clickElement('Rögzít')
            self.html.switchFrame('iframe')
            self.html.clickElement('dc_is_percent', 'label', options=Options(htmlAttribute='data-name'))

            for day in self.days:
                self.html.fillInput(day, self.discountWhite, 'input', options=Options(htmlAttribute='data-title'))

            self.html.clickElement('Rögzít')

            self.clientAssert.assertDiscountCardExist(self.nameWhite, self.codeWhite, self.discountWhite,
                                                      group=self.productGroupWhite, category='Ital')
            # self.clientseed.deleteCard(data.DiscountCard['White Friday']['Name'])

        super(DiscountCards, self).runTest(wrapper, 'discountCards-testCreateCardGroup')

    def testCreateCardProduct(self):
        def wrapper():
            self.html.clickElement('Új kedvezménykártya', 'a')
            self.html.switchFrame('iframe')

            self.html.fillInput('Megnevezés', self.nameWhite)
            self.html.fillInput('Kód', self.codeWhite)

            self.html.clickDropdown('Kategóriák', self.categoryWhite)
            self.html.clickElement('Kategóriák', 'label')
            self.html.clickElement('Termékcsoportok', 'label', options=Options(following='input'))
            self.html.switchFrame('iframe')
            self.html.clickElement(self.productGroupWhite, 'a')
            self.html.clickElement('Rögzít')
            self.html.switchFrame('iframe')
            self.html.clickDropdown('Termékek', self.productWhite) # itt majd lehet egy keresest be kell epiteni
            self.html.clickElement('Termékek', 'label')
            self.html.clickElement('dc_is_percent', 'label', options=Options(htmlAttribute='data-name'))

            for day in self.days:
                self.html.fillInput(day, self.discountWhite, 'input', options=Options(htmlAttribute='data-title'))

            self.html.clickElement('Rögzít')

            self.clientAssert.assertDiscountCardExist(self.nameWhite, self.codeWhite, self.discountWhite,
                                                      group=self.productGroupWhite, category='Ital',
                                                      products=self.productWhite)
            # self.clientseed.deleteCard(data.DiscountCard['White Friday']['Name'])

        super(DiscountCards, self).runTest(wrapper, 'discountCards-testCreateCardProduct')


