import sys
from datetime import datetime

from shared.TestData import TestData as data
from shared.BaseTestCase import BaseTestCase


class Partners(BaseTestCase):
    partnerName = data.Partner['Szallito']['Name']
    partnerId = data.Partner['Szallito']['Id']

    @classmethod
    def setUpClass(self):
        def wrapper():
            super().setUpClass()
            super().login(self)
            self.menu.openReceiving()
            self.html.clickElement('Beszállítók', 'a')

        super(Partners, self).runTest(wrapper, 'partners-setUpClass')

    @classmethod
    def tearDownClass(self):
        def wrapper():
            super().tearDownClass()

        super(Partners, self).runTest(wrapper, 'partners-tearDownClass')

    def tearDown(self):
        try:
            self.receivingseed.deleteParter(self.partnerName, module=True)
        except Exception:
            pass

    def testCreate(self):
        super(Partners, self).runTest(lambda: self.receivingseed.createPartner(self.partnerName, self.partnerId), 'partners-testCreate')

