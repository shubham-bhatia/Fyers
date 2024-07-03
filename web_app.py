import csv
import os

from flask import Flask, request, redirect, url_for, render_template, flash

import BO_Orders
import Orders
import accessTOTP
import cancel_pending_orders
import getPos
import quotes
from cancel_pending_orders import close_all_pending_orders  # Import the new module

APP_ID = accessTOTP.APP_ID
access_token = accessTOTP.main()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

UPLOAD_FOLDER = 'uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            data.append({'symbol': row[0], 'qty': int(row[1]), 'limitPrice': float(row[2]), 'stopLoss': float(row[3]),
                         'side': int(row[4]), 'productType': row[5], 'type': row[6]})
    return data


def make_multiple_of_10(x):
    return round(x * 10) / 10  # Rounds down to nearest 10 and then multiples by 10


def getTradeToOpen(file_path, offlineOrder):
    csv_data = read_csv_file(file_path)
    for trade in csv_data:
        symbol = trade['symbol']
        if "#" not in symbol:
            qty = trade['qty']
            limitPrice = trade['limitPrice']
            # stopLoss = trade['stopLoss']
            side = trade['side']
            productType = trade['productType']
            type = trade['type']

            entryPrice = make_multiple_of_10(limitPrice + (limitPrice * 0.007))
            stopLoss = make_multiple_of_10(entryPrice + (entryPrice * 0.012))  # stopLoss
            calcPrice = (stopLoss - entryPrice) * 1.5
            takeProfit = make_multiple_of_10(entryPrice - calcPrice)  # Target
            tp = make_multiple_of_10(entryPrice - takeProfit)

            print(f"Processing trade for symbol: {symbol} and Product: {productType} and Stop Loss: {stopLoss}")
            resp1 = Orders.openNewOrder(symbol, qty, entryPrice, (stopLoss - entryPrice), side, productType, type, APP_ID,
                                        access_token, offlineOrder, tp)

            flash(resp1)
            # resp2 = Orders.openNewOrder(symbol, qty, limitPrice1, stopLoss, 1, 'INTRADAY', 1, APP_ID, access_token,
            #                             offlineOrder)
            # resp3 = Orders.openNewOrder(symbol, qty, takeProfit, stopLoss, 1, 'INTRADAY', 1, APP_ID, access_token,
            #                             offlineOrder)

            # flash(resp2)
            # flash(resp3)


def getTradeToOpen2(desktop_path, symbol, qty, entryPrice, offlineOrder, mode):
    # entryPrice = make_multiple_of_10(limitPrice + (limitPrice * 0.007))
    entryPrice = make_multiple_of_10(entryPrice)
    stopLoss = make_multiple_of_10(entryPrice + (entryPrice * 0.012))  # stopLoss
    calcPrice = (stopLoss - entryPrice) * 1.5
    takeProfit = make_multiple_of_10(entryPrice - calcPrice)  # Target
    tp = make_multiple_of_10(entryPrice - takeProfit)

    print(f'Entry Price: {entryPrice} Stop Loss: {stopLoss} Take Profit: {tp}')

    resp1 = Orders.openNewOrder(symbol, qty, entryPrice, (stopLoss - entryPrice), -1, "BO", 1, APP_ID, access_token, offlineOrder, tp)

    # limitPrice1 = make_multiple_of_10(limitPrice + (limitPrice * 0.012))  # stopLoss
    # calcPrice = (limitPrice1 - limitPrice) * 1.5
    # takeProfit = make_multiple_of_10(limitPrice - calcPrice)  # Target

    flash(resp1)
    return resp1
    # if mode == 2:
    #     resp2 = Orders.openNewOrder(symbol, qty, limitPrice1, 0, 1, 'INTRADAY', 1, APP_ID, access_token, offlineOrder)
    #     resp3 = Orders.openNewOrder(symbol, qty, takeProfit, 0, 1, 'INTRADAY', 1, APP_ID, access_token, offlineOrder)
    #     flash(resp2)
    #     flash(resp3)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('Please select the file')
        return redirect(url_for('index'))
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        getTradeToOpen(file_path,False)
        flash('File successfully uploaded and processed')
        return redirect(url_for('index'))


@app.route('/action', methods=['POST'])
def perform_action():
    selected_option = request.form.get('option')
    if selected_option:
        selected_value = int(selected_option)
        if selected_value == 1:
            # desktop_path = os.path.join('uploaded_files', 'Trade.txt')
            desktop_path = os.path.join('C:', os.sep, 'Users', 'SHUBHBHATIA', 'Desktop', 'Trade.txt')
            passcode = request.form.get('passcode')
            if passcode == '1':  # Replace 'your_passcode_here' with the actual passcode
                flash('Opening new trade...')
                # desktop_path = os.path.join('C:', os.sep, 'Users', 'SHUBHBHATIA', 'Desktop', 'Trade.txt')
                getTradeToOpen(desktop_path, False)
            else:
                flash('Incorrect passcode.')  # getTradeToOpen(desktop_path)
        elif selected_value == 2:
            # flash('Showing open positions...')
            return redirect(url_for('show_positions'))
        elif selected_value == 3:
            flash('Canceling all orders...')
            close_all_pending_orders(APP_ID, access_token)  # Call the new function
        elif selected_value == 4:
            # flash('Showing order book...')
            return redirect(url_for('show_orderbook'))
        elif selected_value == 5:
            # flash('Showing pending BO orders...')
            return redirect(url_for('show_pending_bo_orders'))
    return redirect(url_for('index'))


@app.route('/positions')
def show_positions():
    positions = getPos.getOpenPositions(APP_ID, access_token)
    total_realized_profit = sum(position['realized_profit'] for position in positions)
    total_unrealized_profit = sum(position['unrealized_profit'] for position in positions)
    Total_pl = total_realized_profit + total_unrealized_profit
    return render_template('positions.html', positions=positions, total_realized_profit=total_realized_profit, total_unrealized_profit=total_unrealized_profit, Total_pl=Total_pl)


@app.route('/orderbook')
def show_orderbook():
    orderbook = Orders.getOrderbook(APP_ID, access_token)
    return render_template('orderbook.html', orderbook=orderbook)


@app.route('/pending_bo_orders')
def show_pending_bo_orders():
    pending_orders = BO_Orders.getPendingBOOrders(APP_ID, access_token)
    # print(quotes.get_quotes(APP_ID, access_token, "NSE:MOTHERSON-EQ"))
    return render_template('pending_bo_orders.html', pending_orders=pending_orders)


@app.route('/cancel_order/<order_id>')
def cancel_order(order_id):
    flash('Order Cancelled: ', order_id)
    cancel_order = cancel_pending_orders.close_Pending_Order(APP_ID, access_token, order_id)
    return redirect(url_for('show_pending_bo_orders'))


@app.route('/cancel__all_orders')
def cancel_all_orders():
    close_all_pending_orders(APP_ID, access_token)
    return redirect(url_for('show_pending_bo_orders'))

@app.route('/close_pos/<pos_id>')
def close_pos(pos_id):
    closePos = getPos.closeOpenPositions(APP_ID, access_token, pos_id)
    flash('Close Position: ', pos_id)
    return redirect(url_for('show_positions'))


@app.route('/new_order', methods=['POST'])
def new_order():
    return redirect(url_for('order_form'))

@app.route('/order_form', methods=['GET', 'POST'])
def order_form():
    if request.method == 'POST':
        symbol = request.form['script']
        qty = request.form['qty']
        entry_price = request.form['entry_price']
        desktop_path = os.path.join('C:', os.sep, 'Users', 'shubhbhatia', 'Desktop', 'Trade.txt')
        selected_option = request.form.get('option')
        mode = request.form.get('mode')
        if mode == 1:
            mode = True
        else:
            mode = False
        response = getTradeToOpen2(desktop_path, symbol, qty, float(entry_price), mode, selected_option)

        return render_template('order_success.html', script=symbol, qty=qty, limit_price=entry_price, response=response)

    return render_template('order_form.html')


# @app.route('/get_ltp', methods=['POST'])
# def get_ltp():
#     script = request.json['script']
#     data = {
#         "symbols": f"NSE:{script}-EQ"
#     }
#     getLTP.getLTP(APP_ID, access_token, data)

if __name__ == '__main__':
    app.run(debug=True)
