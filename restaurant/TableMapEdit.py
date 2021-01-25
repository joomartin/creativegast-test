from core.Options import Options
from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as data


class TableMapEdit(BaseTestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.menu.openTableMapEditor()

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        pass

    def testCreateTable(self):
        self.restaurantseed.createTable(data.Table['Normal']['Name'])
        self.restaurantAssert.assertTableExists(data.Table['Normal']['Name'])
        self.restaurantseed.deleteTable(data.Table['Normal']['Name'])

    def testEdit(self):
        modifiedName = 'Kerek asztal'

        self.restaurantseed.createTable(data.Table['Normal']['Name'])
        self.restaurantAssert.assertTableExists(data.Table['Normal']['Name'])

        self.html.clickElement(data.Table['Normal']['Name'], 'i')
        self.html.fillInput('Asztal neve', modifiedName)
        self.html.clickElement('Rögzít', 'span')
        self.restaurantAssert.assertTableExists(modifiedName)

        self.restaurantseed.deleteTable(modifiedName)

    def testCreateCourier(self):

        self.restaurantseed.createTable(data.Table['Courier']['Name'], tableType='Futár')
        self.restaurantAssert.assertTableExists(data.Table['Courier']['Name'])
        self.restaurantseed.deleteTable(data.Table['Courier']['Name'])


    def testCreateBossTable(self):
        self.restaurantseed.createTable(data.Table['Boss']['Name'], tableShape='Téglalap' ,tableType='Főnöki')
        self.restaurantAssert.assertTableExists(data.Table['Boss']['Name'])
        self.restaurantseed.deleteTable(data.Table['Boss']['Name'])