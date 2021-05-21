from stock.StockController import StockController
from products.ProductController import ProductController
from receiving.ReceivingController import ReceivingController
from restaurant.RestaurantController import RestaurantController
from clientManagement.ClientManagementController import ClientManagementController
from users.UsersController import UsersController

sc = StockController()
pc = ProductController()
rc = ReceivingController()
resc = RestaurantController()
cm = ClientManagementController()
us = UsersController()

sc.run()
#pc.run()
rc.run()
#resc.run()
cm.run()
#us.run()




