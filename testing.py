from config import config
from binance.client import Client

#print(config['api_key'])

BASE_URL = "https://api.binance.com/api/v3"
PUBLIC_URL = "https://www.binance.com/exchange/public/product"

client = Client(config['api_key'], config['secret_key'])
client.ping()

#info = client.get_exchange_info()
info = client.get_symbol_info('BNBBTC')
print(info)
