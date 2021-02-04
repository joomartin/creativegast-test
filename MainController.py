from stock.StockController import StockController
from products.ProductController import ProductController
from receiving.ReceivingController import ReceivingController
from restaurant.RestaurantController import RestaurantController

sc = StockController()
pc = ProductController()
rc = ReceivingController()
resc = RestaurantController()

#sc.run()
#pc.run()
rc.run()
#resc.run()
