import json
from fyers_apiv3 import fyersModel
import accessTOTP

APP_ID = accessTOTP.APP_ID
access_token = accessTOTP.main()
fyers = fyersModel.FyersModel(client_id=APP_ID, token=access_token,is_async=False, log_path="")

def getTradeToOpen():
    file = open("C:\Users\shubhbhatia\Desktop\Trade.txt").readlines()
    developer_id = ""

    for lines in file:
        if 'Developer ID' in lines:
            developer_id = lines.split(":")[-1].strip()

    print
    developer_id
def openNewOrder():
    symbol = input("Symbol: " or "jublfood")
    symbol = "NSE:"+symbol.upper()+"-EQ"
    print(symbol)

    # 1	Limit order
    # 2	Market order
    # 3	Stop order (SL-M)
    # 4	Stoplimit order (SL-L)

    # INTRADAY
    # CO
    # BO

    # type = input("Type (1-LO 2-MO 3-SL/M 4-SL/L): ")
    qty = int(input("Qty: ") or 1)
    # price = input("Price: ")
    limitPrice = input("Limit Price: ")
    # stopPrice = input("Stop Price: ")
    stopLoss = input("Stop Loss: ")
    # takeProfit = input("Take Profit: ")
    # side = input("Side (1-Buy 2-Sell): ")
    # productType = input("Product Type (Intraday/CO/BO): ")

    data = {
        "symbol":symbol,
        "qty":int(qty),
        "type":1,
        "side":-1,
        "productType":"CO",   #productType.upper(),
        # "price":float(price),
        "limitPrice":float(limitPrice),
        # "stopPrice":0,
        # "takeProfit": 0,
        "validity":"DAY",
        "disclosedQty":0,
        "offlineOrder":False,
        # "orderTag":"tag1",
        "stopLoss":float(stopLoss)
    }
    print(data)
    response = fyers.place_order(data=data)
    print(response)

def getOrderbook():

    fyers = fyersModel.FyersModel(client_id=APP_ID, token=access_token, is_async=False, log_path="")
    response = fyers.orderbook()
    parsed_data = json.loads(json.dumps(response))

    # 1 = > Canceled
    # 2 = > Traded / Filled
    # 3 = > (Not used currently)
    # 4 = > Transit
    # 5 = > Rejected
    # 6 = > Pending
    # 7 = > Expired

    _orderNo = 1
    for net_position in parsed_data['orderBook']:
        print('Order: ', _orderNo)
        if net_position['side'] == -1:
            side = 'Sell'
        else:
            side = 'Buy'

        if net_position['status'] == 6:
            status = "Pending"
        elif net_position['status'] == 2:
            status = "Completed"
        else:
             status = net_position['status']
        print('Symbol: ', net_position['symbol']
              , '|| Qty: ', net_position['qty']
              , '|| Limit Price: ', net_position['limitPrice']
              , '|| Stop Price: ', net_position['stopPrice']
              , '|| Side: ', side
              , '|| productType: ', net_position['productType']
              # , '|| orderDateTime: ', net_position['orderDateTime']
              , '|| Status: ', status
              , '|| Type: ', (net_position['type'] , "(1-LO 2-MO 3-SL/M 4-SL/L)")
             )
        _orderNo = _orderNo + 1

# getOrderbook()
getTradeToOpen()
print('--------Lets create a New Order:------------')
# openNewOrder()
