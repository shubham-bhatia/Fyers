import json
from fyers_apiv3 import fyersModel
# import accessTOTP
import json
import csv
import os

# APP_ID = accessTOTP.APP_ID
# access_token = accessTOTP.main()
# fyers = fyersModel.FyersModel(client_id=APP_ID, token=access_token,is_async=False, log_path="")

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        # next(csv_reader)  # Skip the header row
        for row in csv_reader:
            data.append(row)
    return data

def getTradeToOpen():
    desktop_path = os.path.join('C:', os.sep, 'Users', 'shubhbhatia', 'Desktop', 'Trade.txt')
    csv_data = read_csv_file(desktop_path)
    print(csv_data)
    print(type(csv_data))

    for i in range(len(csv_data)):
        print(csv_data[i])
        print(type(csv_data[i]))

    # for idx, row in enumerate(csv_data, 1):
    #     symbol = row[0]
        # qty = row[0]
        # LP = row[2]
        # SL = row[3]
        # return symbol#, qty, LP, SL
        # print(f"Processing record {idx}/{len(csv_data)}")

def openNewOrder(symbol, qty, limitPrice, stopLoss, APP_ID, access_token):

    # getTradeToOpen()

    # symbol = input("Symbol: " or "jublfood")
    symbol = "NSE:"+symbol.upper()+"-EQ"
    # print(symbol)

    # 1	Limit order
    # 2	Market order
    # 3	Stop order (SL-M)
    # 4	Stoplimit order (SL-L)

    # INTRADAY
    # CO
    # BO

    # type = input("Type (1-LO 2-MO 3-SL/M 4-SL/L): ")
    # qty = int(input("Qty: ") or "1")
    # price = input("Price: ")
    # limitPrice = input("Limit Price: ")
    # stopPrice = input("Stop Price: ")
    # stopLoss = input("Stop Loss: ")
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
        # "stopPrice":float(stopLoss),
        # "takeProfit": 0,
        "validity":"DAY",
        "disclosedQty":0,
        "offlineOrder":False,
        # "orderTag":"Python",
        "stopLoss":float(stopLoss)
    }
    print(data)
    fyers = fyersModel.FyersModel(client_id=APP_ID, token=access_token,is_async=False, log_path="")
    response = fyers.place_order(data=data)
    print(response)

def getOrderbook(APP_ID, access_token):

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
        if net_position['side'] == -1:
            side = 'Sell'
        else:
            side = 'Buy'

        if net_position['status'] == 6:

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
# getTradeToOpen()
# print('--------Lets create a New Order:------------')
# openNewOrder()
