
from shared.TestData import TestData as data
from shared.BaseTestCase import BaseTestCase


class Partners(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)
        self.menu.openReceiving()
        self.html.clickElement('Beszállítók', 'a')

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def testCreate(self):
        partnerName = data.Partner['Szallito']['Name']
        partnerId = data.Partner['Szallito']['Id']
        self.receivingseed.createPartner(partnerName, partnerId)
        self.receivingseed.deleteParter(partnerName)

