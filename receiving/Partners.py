import sys
from datetime import datetime

from shared.TestData import TestData as data
from shared.BaseTestCase import BaseTestCase


class Partners(BaseTestCase):
    partnerName = data.Partner['Szallito']['Name']
    partnerId = data.Partner['Szallito']['Id']

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)
        self.menu.openReceiving()
        self.html.clickElement('Beszállítók', 'a')

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]

    def tearDown(self):
        try:
            self.receivingseed.deleteParter(self.partnerName, module=True)
        except Exception:
            pass

    def testCreate(self):
        try:
            self.receivingseed.createPartner(self.partnerName, self.partnerId)
        except Exception as e:
            now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            self.driver.get_screenshot_as_file('.//screenShots/screenshot-%s.png' % now)
            raise e



