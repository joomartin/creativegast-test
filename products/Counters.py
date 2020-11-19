from shared.BaseTestCase import BaseTestCase

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
        counter = 'test_counter'
        position = 3

        self.productseed.createCounter(counter, position)
        self.productAssert.assertCounterExists(counter, 'Számlálók')
        self.html.search(counter, 'Számlálók')
        obsPos = self.html.getTxtFromTable('1', '3', 'counters')
        self.assertEqual(int(float(obsPos)), position)
        self.html.search('', 'Számlálók')

        self.productseed.deleteCounter(counter)
        self.productAssert.assertCounterNotExists(counter, 'Számlálók')
        self.html.search('', 'Számlálók')

    def testDetails(self):
        counter = 'test_counter'
        position = 3

        self.productseed.createCounter(counter, position)

        self.html.clickTableElement('counters', 'id', counter, 'a', 'Részletek', 'Számlálók')
        self.html.switchFrame('iframe')

        obsCounter = self.html.getTxtFromTable('1', '1')
        self.assertEqual(obsCounter, counter)
        obsPos = self.html.getTxtFromTable('2', '1')
        self.assertEqual(int(obsPos), position)

        self.productseed.deleteCounter(counter)
        self.html.search('', 'Számlálók')

    def testEdit(self):
        counter = 'test_counter'
        position = 3

        newCounter = 'new_counter'
        newPosition = 7

        self.productseed.createCounter(counter, position)

        self.html.clickTableElement('counters', 'id', counter, 'a', 'Szerkeszt', 'Számlálók')
        self.html.switchFrame('iframe')

        self.html.fillInput('Számláló neve', newCounter)
        self.html.fillInput('Számláló állás', newPosition)
        self.html.clickElement('Rögzít')
        self.html.switchFrame()

        self.productAssert.assertCounterExists(newCounter, 'Számlálók')
        self.html.search(newCounter, 'Számlálók')
        obsPos = self.html.getTxtFromTable('1', '3', 'counters')
        self.assertEqual(int(float(obsPos)), newPosition)

        self.productseed.deleteCounter(newCounter)
        self.html.search('', 'Számlálók')
