import getPos
import accessTOTP
import Orders

APP_ID = accessTOTP.APP_ID
access_token = accessTOTP.main()


symbol = input("Symbol: ")
qty = input("Qty: ")
limitPrice = input("Limit Price: ")
stopLoss = input("Stop Loss: ")

# get all open positions
# getPos.getOpenPositions(APP_ID, access_token)

# Orders.getOrderbook(APP_ID, access_token)
Orders.openNewOrder(symbol, qty, limitPrice, stopLoss, APP_ID, access_token)