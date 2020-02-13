import requests
import json

# Get Bitcoin Price
def get_btc():
    bitcoin_price_request = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
    bitcoin_price = json.loads(bitcoin_price_request.content)
    bitcoin_price = bitcoin_price['USD']
    return bitcoin_price

# Get BTC Full Data
def symbol():
    symbol_request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USD')
    symbol = json.loads(symbol_request.content)
    return symbol

'''
def numbers():
    my_number = 4385893.38
    my_number_2 = 123456789.87
    list = [my_number, my_number_2]
    for member in list:
        form = '{:,.2f}'.format(member)
        return form

print(numbers())

my_number = 4385893.38
my_number_2 = 123456789.87
list = [my_number, my_number_2]
for member in list:
    form = '{:,.2f}'.format(member)
    print(form)

'''
'''
list = [0.34555, 0.2323456, 0.6234232, 0.45234234]
for member in list:
    form='{:.1%}'.format(member)


#my_string = '{:,.2f}'.format(my_number)
#print(my_string)
'''