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
        table = self.html.getElement('barchecking', 'table', Options(htmlAttribute='id'))
        table.find_element_by_xpath('.//a[contains(., "Törlés")]').click()
        self.html.clickElement('Igen')
        self.html.refresh()

    def testCreate(self):
        self.createBarChecking()

        table = self.html.getElement('barchecking', 'table', Options(htmlAttribute='id'))
        table.find_element_by_xpath('.//a[contains(., "Megtekintés")]').click()

        self.html.switchFrame('iframe')

        summMiss = self.html.getTxtFromTable(3, 4)
        self.assertEqual(summMiss, '-5')

        colaMiss = self.html.getTxtFromTable(3, 4)
        self.assertEqual(colaMiss, '-5')

        self.html.clickElement('Mégsem')
        self.html.switchFrame()

        self.deleteChecking()

