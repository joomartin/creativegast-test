from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data


class TableMapEdit(BaseTestCase):
    modifiedName = 'Kerek asztal'

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openTableMapEditor()

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def tearDown(self):
        try:
            self.restaurantseed.deleteTable(data.Table['Normal']['Name'])
        except Exception:
            pass
        try:
            self.restaurantseed.deleteTable(self.modifiedName)
        except Exception:
            pass
        try:
            self.restaurantseed.deleteTable(data.Table['Courier']['Name'])
        except Exception:
            pass
        try:
            self.restaurantseed.deleteTable(data.Table['Boss']['Name'])
        except Exception:
            pass

    def testCreateTable(self):
        def wrapper():
            self.restaurantseed.createTable(data.Table['Normal']['Name'])
            self.restaurantAssert.assertTableExists(data.Table['Normal']['Name'])

        super(TableMapEdit, self).runTest(wrapper, 'tablemapedit-testCreateTable')

    def testEdit(self):
        def wrapper():
            self.restaurantseed.createTable(data.Table['Normal']['Name'])
            self.restaurantAssert.assertTableExists(data.Table['Normal']['Name'])

            self.html.clickElement(data.Table['Normal']['Name'], 'i')
            self.html.fillInput('Asztal neve', self.modifiedName)
            self.html.clickElement('Rögzít', 'span')
            self.restaurantAssert.assertTableExists(self.modifiedName)

        super(TableMapEdit, self).runTest(wrapper, 'tablemapedit-testEdit')

    def testCreateCourier(self):
        def wrapper():
            self.restaurantseed.createTable(data.Table['Courier']['Name'], tableType='Futár')
            self.restaurantAssert.assertTableExists(data.Table['Courier']['Name'])

        super(TableMapEdit, self).runTest(wrapper, 'tablemapedit-testCreateCourier')

    def testCreateBossTable(self):
        def wrapper():
            self.restaurantseed.createTable(data.Table['Boss']['Name'], tableShape='Téglalap', tableType='Főnöki')
            self.restaurantAssert.assertTableExists(data.Table['Boss']['Name'])

        super(TableMapEdit, self).runTest(wrapper, 'tablemapedit-testCreateBossTable')

