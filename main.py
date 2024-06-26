import os
import getPos
import Orders
import accessTOTP

APP_ID = accessTOTP.APP_ID
access_token = accessTOTP.main()


def readFile():
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
    # readFile()

    # get all open positions
    getPos.getOpenPositions(APP_ID, access_token)
    print('----------------------------------------------######################------------------------------------')
    Orders.getOrderbook(APP_ID, access_token)
    # Orders.openNewOrder(symbol, qty, limitPrice, stopLoss, APP_ID, access_token)
