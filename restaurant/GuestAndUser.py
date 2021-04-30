from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from selenium.webdriver.common.keys import Keys
from core.Options import Options

class GuestAndUser(BaseTestCase):
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
    address = data.Client['Pista']['Street']

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def testCreateUser(self):
        surname = data.User['Géza']['Surname']
        firstName = data.User['Géza']['FirstName']
        userName = data.User['Géza']['UserName']
        position = data.User['Géza']['Position']
        password = data.User['Géza']['Password']
        group = data.User['Géza']['Group']
        rights = data.Group['Felszolgáló2']['Rights'].values()

        self.menu.openUsers()

        self.usersSeed.createUser(surname, firstName, userName, password, position, group)
        self.menu.openUsers()
        self.usersAssert.assertUserExist(surname, firstName, position, rights, group=group)

        self.html.clickElement('Kilépés a rendszerből', 'a')
        self.html.fillInput('Felhasználónév', userName, selector='placeholder')
        self.html.fillInput('Jelszó', password, selector='placeholder')
        self.html.clickElement('Belépés')
        self.html.fillInput('Belépési kód', password, selector='placeholder')
        self.html.clickElement('Belépés')
        self.menu.openUsers()

        self.html.clickElement('Kilépés a rendszerből', 'a')
        super().setUpClass()
        super().login()
        self.menu.openUsers()

        self.usersSeed.deleteUser(surname)

    def testCreateRegular(self):

        self.menu.openClientManagement()
        self.html.clickElement('Törzsvendégek', 'a')
        self.clientAssert.assertRegularExist(self.name, self.address, self.phone, self.discount, self.code)

        self.clientseed.deleteRegular(self.name)