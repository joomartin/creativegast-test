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
        self.restaurantseed.createTable('Teszt asztal')
        self.restaurantAssert.assertTableExists('Teszt asztal')
        self.restaurantseed.deleteTable('Teszt asztal')

    def testEdit(self):
        modifiedName = 'Kerek asztal'

        self.restaurantseed.createTable('Teszt asztal')
        self.restaurantAssert.assertTableExists('Teszt asztal')

        self.html.clickElement('Teszt asztal', 'i')
        self.html.fillInput('Asztal neve', modifiedName)
        self.html.clickElement('Rögzít', 'span')
        self.restaurantAssert.assertTableExists(modifiedName)

        self.restaurantseed.deleteTable(modifiedName)

    def testCreateCourier(self):

        self.restaurantseed.createTable('NetPincér', tableType='Futár')
        self.restaurantAssert.assertTableExists('NetPincér')
        self.restaurantseed.deleteTable('NetPincér')


    def testCreateBossTable(self):
        self.restaurantseed.createTable('Boss', tableShape='Téglalap' ,tableType='Főnöki')
        self.restaurantAssert.assertTableExists('Boss')
        self.restaurantseed.deleteTable('Boss')