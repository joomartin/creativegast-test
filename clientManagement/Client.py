
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options


class Regulars(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

    def setUp(self):
        self.menu.openClientManagement()

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def tearDown(self):
        pass

    def testCreateClient(self):
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
        address = self.clientseed.createClient(name, code, phone, discount, taxnumber, country, postalCode, city, street, housenumber)

        self.clientAssert.assertClientExist(name, address, phone,
                                            discount, code)

        self.clientseed.deleteClient(name)






















