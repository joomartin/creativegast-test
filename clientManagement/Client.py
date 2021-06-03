
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data
from core.Options import Options


class Regulars(BaseTestCase):
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
        try:
            self.clientseed.deleteClient(self.name, module=True)
        except Exception:
            pass

    def testCreateClient(self):

        address = self.clientseed.createClient(self.name, self.code, self.phone, self.discount, self.taxnumber,
                                               self.country, self.postalCode, self.city, self.street, self.housenumber,
                                               module=True)

        self.clientAssert.assertClientExist(self.name, address, self.phone, self.discount, self.code)






















