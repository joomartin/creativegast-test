
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data


class TableMapEdit(BaseTestCase):
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
        address = self.clientseed.createRegular(self.name, self.code, self.phone, self.discount, self.taxnumber, self.country, self.postalCode, self.city,
                                                self.street, self.housenumber, module=True)

        self.menu.openRestaurant()
        self.html.clickElement('Dinamikus futár asztalok', 'a')

    @classmethod
    def tearDownClass(self):
        #super().tearDownClass()
        pass

    def testCreateTable(self):
        self.restaurantseed.createDynamicCourierTable(self.name)
        self.html.wait(5)




































