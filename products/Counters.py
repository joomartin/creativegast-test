from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data

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

        self.productseed.createCounter(data.Counter['TestCounter']['Name'], data.Counter['TestCounter']['Position'])
        self.productAssert.assertCounterExists(data.Counter['TestCounter']['Name'], 'Számlálók')
        self.html.search(data.Counter['TestCounter']['Name'], 'Számlálók')
        obsPos = self.html.getTxtFromTable('1', '3', 'counters')
        self.assertEqual(str(int(float(obsPos))), data.Counter['TestCounter']['Position'])
        self.html.search('', 'Számlálók')

        self.productseed.deleteCounter(data.Counter['TestCounter']['Name'])
        self.productAssert.assertCounterNotExists(data.Counter['TestCounter']['Name'], 'Számlálók')
        self.html.search('', 'Számlálók')

    def testDetails(self):

        self.productseed.createCounter(data.Counter['TestCounter']['Name'], data.Counter['TestCounter']['Position'])

        self.html.clickTableElement('counters', 'id', data.Counter['TestCounter']['Name'], 'a', 'Részletek', 'Számlálók')
        self.html.switchFrame('iframe')

        obsCounter = self.html.getTxtFromTable('1', '1')
        self.assertEqual(obsCounter, data.Counter['TestCounter']['Name'])
        obsPos = self.html.getTxtFromTable('2', '1')
        self.assertEqual(str(int(obsPos)), data.Counter['TestCounter']['Position'])

        self.productseed.deleteCounter(data.Counter['TestCounter']['Name'])
        self.html.search('', 'Számlálók')

    def testEdit(self):
        modifiedName = 'ModifiedCounter'
        modifiedPosition = 7

        self.productseed.createCounter(data.Counter['TestCounter']['Name'], data.Counter['TestCounter']['Position'])

        self.html.clickTableElement('counters', 'id', data.Counter['TestCounter']['Name'], 'a', 'Szerkeszt', 'Számlálók')
        self.html.switchFrame('iframe')

        self.html.fillInput('Számláló neve', modifiedName)
        self.html.fillInput('Számláló állás', modifiedPosition)
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

        self.productAssert.assertCounterExists(modifiedName, 'Számlálók')
        self.html.search(modifiedName, 'Számlálók')
        obsPos = self.html.getTxtFromTable('1', '3', 'counters')
        self.assertEqual(str(int(float(obsPos))), str(modifiedPosition))

        self.productseed.deleteCounter(modifiedName)
        self.html.search('', 'Számlálók')
