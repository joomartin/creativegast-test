import os

from stock.StockController import StockController

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

sc = StockController()
sc.run()
