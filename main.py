import getPos
import accessTOTP
import Orders

APP_ID = accessTOTP.APP_ID
access_token = accessTOTP.main()

# get all open positions
# getPos.getOpenPositions(APP_ID, access_token)

# Orders.getOrderbook(APP_ID, access_token)
Orders.openNewOrder("ioc", 1, 174, 190, APP_ID, access_token)