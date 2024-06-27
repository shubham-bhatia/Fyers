import csv
import os
import getPos
import Orders
import accessTOTP

APP_ID = accessTOTP.APP_ID
access_token = accessTOTP.main()

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            data.append({
                'symbol': row[0],
                'qty': int(row[1]),
                'limitPrice': float(row[2]),
                'stopLoss': float(row[3]),
                'side': int(row[4]),
                'productType': row[5],
                'type': row[6]
            })
    return data


def getTradeToOpen(file_path):
    csv_data = read_csv_file(file_path)
    for trade in csv_data:
        symbol = trade['symbol']
        if "#" not in symbol:
            qty = trade['qty']
            limitPrice = trade['limitPrice']
            stopLoss = trade['stopLoss']
            side = trade['side']
            productType = trade['productType']
            type = trade['type']

            print(f"Processing trade for symbol: {symbol} and Product: {productType}")
            Orders.openNewOrder(symbol, qty, limitPrice, stopLoss, side, productType, type, APP_ID, access_token,True)


def readFileToOpenNewOrder():
    desktop_path = os.path.join('C:', os.sep, 'Users', 'shubhbhatia', 'Desktop', 'Trade.txt')
    with open(desktop_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split(',')

        symbol = parts[0].strip()
        qty = int(parts[1].strip())
        limitPrice = float(parts[2].strip())
        stopLoss = float(parts[3].strip())

        Orders.openNewOrder(symbol, qty, limitPrice, stopLoss, APP_ID, access_token)

    # symbol = lines[0].strip()
    # qty = int(lines[1].strip())
    # limitPrice = float(lines[2].strip())
    # stopLoss = float(lines[3].strip())
    #
    # return symbol, qty, limitPrice, stopLoss


if __name__ == '__main__':
    # get all open positions
    # getPos.getOpenPositions(APP_ID, access_token)
    print('----------------------------------------------######################------------------------------------')
    # Orders.openNewOrder(symbol, qty, limitPrice, stopLoss, APP_ID, access_token)
    # readFileToOpenNewOrder()
    desktop_path = os.path.join('C:', os.sep, 'Users', 'shubhbhatia', 'Desktop', 'Trade.txt')

    # Orders.getOrderbook(APP_ID, access_token)

    # BO_Orders.getPendingBOOrders(APP_ID, access_token)

    # TOP OPEN NEW TRADE
    getTradeToOpen(desktop_path)
