from stock.StockController import StockController
from products.ProductController import ProductController
from receiving.ReceivingController import ReceivingController

sc = StockController()
pc = ProductController()
rc = ReceivingController()

#sc.run()
#pc.run()
rc.run()
