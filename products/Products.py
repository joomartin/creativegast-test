from core.Options import Options
from shared.BaseTestCase import BaseTestCase

class Products(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openProducts()

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def createProduct(self, name, group, code, counter):
        self.html.clickElement('Új termék felvitele', 'a')
        self.html.switchFrame('iframe')

        self.html.clickDropdown('Nyomtatási részleg', 'Pult')
        self.html.switchFrame('iframe')

        self.html.clickElement(group, 'a')
        self.html.clickElement('Rögzít')

        self.html.switchFrame('iframe')
        self.html.fillInput('Termék neve', name)
        self.html.fillInput('Kód', code)

        self.html.clickElement('p_counters', 'input', Options(htmlAttribute='id'), waitSeconds = 1)
        self.html.switchFrame('iframe')

        self.html.clickElement(counter, 'td')
        self.html.clickElement('Rögzít')
        self.html.switchFrame('iframe')

        asd = self.html.getElement('Eladási ár (Kötelező)', 'td')
        self.html.clickElement('Ár megadása', element=asd)


    def deleteProduct(self):
        pass

    def testCreate(self):
        self.createProduct('01product', 'Szeszes italok', 99, '1asd')

    def testEdit(self):
        pass

    def testDetails(self):
        pass

    def testClone(self):
        pass


































