from selenium.webdriver.common.keys import Keys
from core.Options import Options
from shared.BaseTestCase import BaseTestCase


class BarCheckings(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openStocks()
        self.html.clickElement('Standellenőrzések', 'a')

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def createBarChecking(self):
        self.html.clickElement('Új standellenőrzés', 'a')
        self.html.switchFrame('iframe')

        self.html.clickElement('Pult', 'label', Options(following='label'))
        self.html.clickElement('Indít', waitSeconds=3)

        self.html.fillInput('450.00000', '445', 'value')
        self.html.clickElement('Coca Cola 0.5 l', 'td', Options(following='button'))

        self.html.clickElement('Lezárás', 'a')
        self.html.refresh()

    def deleteChecking(self):
        self.html.clickTableElement('barchecking', 'id', 'Admin Admin', 'a', 'Törlés')
        self.html.clickElement('Igen')
        self.html.refresh()

    def testCreate(self):
        self.createBarChecking()

        self.html.clickTableElement('barchecking', 'id', 'Admin Admin', 'a', 'Megtekintés')

        self.html.switchFrame('iframe')

        summMiss = self.html.getTxtFromTable(3, 4)
        self.assertEqual(summMiss, '-5')

        colaMiss = self.html.getTxtFromTable(3, 4)
        self.assertEqual(colaMiss, '-5')

        self.html.clickElement('Mégsem')
        self.html.switchFrame()

        self.deleteChecking()

