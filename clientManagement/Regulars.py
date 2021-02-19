
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
        self.html.clickElement('Törzsvendégek', 'a')

    @classmethod
    def tearDownClass(self):
        # super().tearDownClass()
        pass

    def tearDown(self):
        pass

    def testCreateRegular(self):
        self.html.clickElement('Új törzsvendég', 'a', waitSeconds=2)

        self.html.switchFrame('iframe')
        self.html.fillInput('Név / azonosító', data.Client['Pista']['Name'])
        self.html.fillInput('Ügyfélazonosító', data.Client['Pista']['Code'])
        self.html.fillInput('Telefon', data.Client['Pista']['Phone'])
        self.html.fillInput('Kedv. (%)', data.Client['Pista']['Discount'])
        self.html.fillInput('Adószám', data.Client['Pista']['TaxNumber'])

        self.html.fillInput('ca_country_helper', data.Client['Pista']['Country'], 'input', options=Options(htmlAttribute='id'))
        self.html.fillInput('ca_zip_helper', data.Client['Pista']['PostalCode'], 'input',
                            options=Options(htmlAttribute='id'))
        self.html.fillInput('ca_city_helper', data.Client['Pista']['City'], 'input',
                            options=Options(htmlAttribute='id'))
        self.html.fillInput('ca_street_helper', data.Client['Pista']['Street'], 'input',
                            options=Options(htmlAttribute='id'))
        self.html.fillInput('ca_housenumber_helper', data.Client['Pista']['HouseNumber'], 'input',
                            options=Options(htmlAttribute='id'))
        self.html.clickElement('Hozzáad')
        self.html.clickElement('Rögzít', waitSeconds=2)
        self.html.switchFrame()

        address = data.Client['Pista']['Country'] + ', ' + data.Client['Pista']['PostalCode'] + ' ' + \
                  data.Client['Pista']['City'] + ' ' + data.Client['Pista']['Street'] + ' ' + data.Client['Pista'][
                      'HouseNumber']

        self.clientAssert.assertClientExist(data.Client['Pista']['Name'], address, data.Client['Pista']['Phone'],
                                            data.Client['Pista']['Discount'], data.Client['Pista']['Code'])



        self.clientseed.deleteClient(data.Client['Pista']['Name'])






















