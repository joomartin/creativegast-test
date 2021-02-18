from stock.StockController import StockController
from products.ProductController import ProductController
from receiving.ReceivingController import ReceivingController
from restaurant.RestaurantController import RestaurantController
from clientManagement.ClientManagementController import ClientManagementController
sc = StockController()
pc = ProductController()
rc = ReceivingController()
resc = RestaurantController()
cm = ClientManagementController()

#sc.run()
#pc.run()
#rc.run()
#resc.run()
cm.run()





