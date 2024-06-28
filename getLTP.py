from fyers_apiv3 import fyersModel


def getLTP(app_id, access_token, data):
    fyers = fyersModel.FyersModel(client_id=app_id, token=access_token)
    response = fyers.quotes(data=data)
    print(response)
    # return response
