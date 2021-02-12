from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options


class DiscountCards(BaseTestCase):
    days = ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap']

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

    def setUp(self):
        self.menu.openClientManagement()
        self.html.clickElement('Kedvezménykártyák', 'a')

    @classmethod
    def tearDownClass(self):
        # super().tearDownClass()
        pass

    def tearDown(self):
        pass

    def testCreateCardDrink(self):
        name = data.DiscountCard['White Friday']['Name']
        code = data.DiscountCard['White Friday']['Code']
        discount = data.DiscountCard['White Friday']['Discount']
        category = data.DiscountCard['White Friday']['Category']

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

    def testCreateCardFood(self):
        name = data.DiscountCard['Blue Friday']['Name']
        code = data.DiscountCard['Blue Friday']['Code']
        discount = data.DiscountCard['Blue Friday']['Discount']
        category = data.DiscountCard['Blue Friday']['Category']

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

    def testCreateCardAll(self):
        name = data.DiscountCard['Blue Friday']['Name']
        code = data.DiscountCard['Blue Friday']['Code']
        discount = data.DiscountCard['Blue Friday']['Discount']
        category = data.DiscountCard['Blue Friday']['Category']

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































