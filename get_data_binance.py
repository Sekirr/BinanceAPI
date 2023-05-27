from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.enums import *
from binance.exceptions import *
# import pandas as pd
import random
import numpy
import pytest



def api_binance( data, symbol ):

	apikey 		= 'cade52fff14399f6bf50fb249493121aaeb6f2f962e344b416c0700c8a2320c7'
	secretkey	= 'f77c6e5dac89e4d5f615e7a6afea10fb36cfbebbb002405d7d6a71bf10fa2757'

	# connect
	client = Client(api_key = apikey, api_secret = secretkey, testnet='true')
	status = client.get_system_status()

	# normal (0: normal; 1: system maintenance)
	if status['status'] == 0:

		side 				= data['side']
		priceMin		= data['priceMin']
		priceMax 		= data['priceMax']
		amountDif 	= data['amountDif']
		volume 			= data['volume']

		price 			= round(random.uniform(priceMin, priceMax), 1)
		sum_orders 	= price * round((volume/price))
		quantity		= round(volume / price)

		while sum_orders <= volume - amountDif or sum_orders >= volume + amountDif:

			price 			= round(random.uniform(priceMin, priceMax), 1)
			quantity		= round(volume / price) 
			sum_orders 	= price * quantity

		try:
			# create orders
			if side == 'SELL':
				take = client.futures_create_order(
						symbol 				= symbol,
						side					= side,
						type					= 'LIMIT',
						quantity			= quantity,
						price					= str(price),
						timeInForce		= 'GTC'
					)
			elif side == 'BUY':
				take = client.futures_create_order(
						symbol 				= symbol,
						side 					= side,
						type 					= 'LIMIT',
						quantity			= quantity,
						price 				= str(price),
						timeInForce 	= 'GTC'
					)
			return True
		except BinanceAPIException as e:
			if 'code=-2027' in str(e):
				print("Условная стоимость выше, чем позволяет кредитное плечо. Выберите другую стоимость или другую валюту")

			return True
	else:
		print('Подключение отсутствует')
		return True


data = {
		'volume': 		10000.0, 	# в долларах
		'number': 		5, 				# на сколько ордеров нужно разбить этот объём
		'amountDif':	50.0,			# разброс в долларах, в пределах которого случайным образом выбирается объём в верхнюю и нижнюю сторону
		'side':				'SELL',		# сторона торговли (SELL или BUY)
		'priceMin':		200.0,		# нижний диапазон цены, в пределах которого нужно случайным образом выбрать цену 
		'priceMax':		300.0,		# верхний диапазон цены, а пределах которого нужно случайным образом выбрать цену
	}
	
symbol = [
	'XMRUSDT'
	'BTCUSDT'
	'ETHUSDT'
]
# @pytest.mark.parametrize('data', data,'symbol', symbol)
def test():
	data = {
		'volume': 		10000.0, 	# в долларах
		'number': 		5, 				# на сколько ордеров нужно разбить этот объём
		'amountDif':	50.0,			# разброс в долларах, в пределах которого случайным образом выбирается объём в верхнюю и нижнюю сторону
		'side':				'SELL',		# сторона торговли (SELL или BUY)
		'priceMin':		200.0,		# нижний диапазон цены, в пределах которого нужно случайным образом выбрать цену 
		'priceMax':		300.0,		# верхний диапазон цены, а пределах которого нужно случайным образом выбрать цену
	}
	result = api_binance(data, 'XMRUSDT')
	assert result == True	

	data = {
		'volume': 		10000.0, 	# в долларах
		'number': 		5, 				# на сколько ордеров нужно разбить этот объём
		'amountDif':	50.0,			# разброс в долларах, в пределах которого случайным образом выбирается объём в верхнюю и нижнюю сторону
		'side':				'SELL',		# сторона торговли (SELL или BUY)
		'priceMin':		159.0,		# нижний диапазон цены, в пределах которого нужно случайным образом выбрать цену 
		'priceMax':		161.0,		# верхний диапазон цены, а пределах которого нужно случайным образом выбрать цену
	}
	assert api_binance(data, 'XMRUSDT') == True	

	data = {
		'volume': 		10000.0, 	# в долларах
		'number': 		5, 				# на сколько ордеров нужно разбить этот объём
		'amountDif':	50.0,			# разброс в долларах, в пределах которого случайным образом выбирается объём в верхнюю и нижнюю сторону
		'side':				'SELL',		# сторона торговли (SELL или BUY)
		'priceMin':		1200.0,		# нижний диапазон цены, в пределах которого нужно случайным образом выбрать цену 
		'priceMax':		1700.0,		# верхний диапазон цены, а пределах которого нужно случайным образом выбрать цену
	}
	assert api_binance(data, 'XMRUSDT') == True	


test()

