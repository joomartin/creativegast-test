from shared.BaseTestCase import BaseTestCase
from shared.TestData import TestData as td

class Conveniences(BaseTestCase):


    @classmethod
    def setUpClass(self):
        super().setUpClass()
        super().login(self)

        self.stockseed.createWarehouse(td.WareHouse['Name'], module=True)
        self.stockseed.createRawMaterial(td.RawMaterial['Name'], td.RawMaterial['ME'], td.WareHouse['Name'],
                                         module=True)
        self.stockseed.createRawMaterial(td.RawMaterial['Name2'], td.RawMaterial['ME'], td.WareHouse['Name'])
        self.productseed.createCounter(td.Counter['Name'], td.Counter['Position'], module=True)
        self.productseed.createProductConveniencies(td.Product['Name'], td.ProductGroup['Conveniences'], td.Product['Code'], td.Counter['Name'], td.RawMaterial['Name'])

        self.menu.openProducts()

    @classmethod
    def tearDownClass(self):
        self.stockseed.deleteRawMaterial(td.RawMaterial['Name'], module=True)
        self.stockseed.deleteRawMaterial(td.RawMaterial['Name2'], module=True)
        self.stockseed.deleteWarehouse(td.WareHouse['Name'], tab=True)
        self.productseed.deleteCounter(td.Counter['Name'], module=True)
        super().tearDownClass()





