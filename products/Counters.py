from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as td

class Counters(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openProducts()
        self.html.clickElement('Számlálók', 'a', waitSeconds = 2)

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def testCreate(self):

        self.productseed.createCounter(td.Counter['Name'], td.Counter['Position'])
        self.productAssert.assertCounterExists(td.Counter['Name'], 'Számlálók')
        self.html.search(td.Counter['Name'], 'Számlálók')
        obsPos = self.html.getTxtFromTable('1', '3', 'counters')
        self.assertEqual(str(int(float(obsPos))), td.Counter['Position'])
        self.html.search('', 'Számlálók')

        self.productseed.deleteCounter(td.Counter['Name'])
        self.productAssert.assertCounterNotExists(td.Counter['Name'], 'Számlálók')
        self.html.search('', 'Számlálók')

    def testDetails(self):

        self.productseed.createCounter(td.Counter['Name'], td.Counter['Position'])

        self.html.clickTableElement('counters', 'id', td.Counter['Name'], 'a', 'Részletek', 'Számlálók')
        self.html.switchFrame('iframe')

        obsCounter = self.html.getTxtFromTable('1', '1')
        self.assertEqual(obsCounter, td.Counter['Name'])
        obsPos = self.html.getTxtFromTable('2', '1')
        self.assertEqual(str(int(obsPos)), td.Counter['Position'])

        self.productseed.deleteCounter(td.Counter['Name'])
        self.html.search('', 'Számlálók')

    def testEdit(self):

        self.productseed.createCounter(td.Counter['Name'], td.Counter['Position'])

        self.html.clickTableElement('counters', 'id', td.Counter['Name'], 'a', 'Szerkeszt', 'Számlálók')
        self.html.switchFrame('iframe')

        self.html.fillInput('Számláló neve', td.Counter['ModifiedName'])
        self.html.fillInput('Számláló állás', td.Counter['ModifiedPosition'])
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

        self.productAssert.assertCounterExists(td.Counter['ModifiedName'], 'Számlálók')
        self.html.search(td.Counter['ModifiedName'], 'Számlálók')
        obsPos = self.html.getTxtFromTable('1', '3', 'counters')
        self.assertEqual(str(int(float(obsPos))), td.Counter['ModifiedPosition'])

        self.productseed.deleteCounter(td.Counter['ModifiedName'])
        self.html.search('', 'Számlálók')
