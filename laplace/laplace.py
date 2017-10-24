from laplace.error import *
from laplace.call import XCoinAPI
from laplace.tracer import Tracer

import logging

def blank_callback():
	pass


class Laplace:
	def __init__(self, spath):
		from os.path import isfile
		import json

		if not isfile(spath):
			raise NoSettingsPathError(spath)
		else:
			with open(spath, 'r') as fp:
				settings = json.loads(fp.read())
				possible_keys = ('key','secret','currency','delay',\
								'log_distance','trace_days')

				if set(possible_keys) != set(settings.keys()):
					raise InvalidSettingsPathKeyError(possible_keys)

		self.core = XCoinAPI(settings['key'], settings['secret'])
		self.currency = settings['currency']
		self.delay = settings['delay']
		self.log_distance = self.convert_distance(settings['log_distance'])

		self.trace_days = settings['trace_days']
		self.tracer = Tracer(master=self)

		self.update()


	def call(self, path, params={}):
		from time import sleep

		while True:
			response = self.core.xcoinApiCall(path, params)

			if response['status']=='5300':
				raise ResponseError('5300','Invalid API KEY.')
			
			elif response['status']=='5100':
				raise ResponseError('5100','Invalid API SECRET/permission level.')
			
			elif response['status']=='5500' and '지원하지 않는 화폐' in response['message']:
				raise ResponseError('5500','Invalid currency {}'.format(self.currency))

			elif response['status']=='5600' and \
								'매수금액이 사용가능 KRW 를 초과' in response['message']:
				logging.critical(str(response))
				sleep(1.5)
				return False

			elif response['status']!='0000':
				logging.critical(str(response))
				sleep(1.5)
				continue

			return response['data']


	def update(self):
	# update current krw and units
		data = self.call(\
			path='/info/balance/',params={'currency': self.currency})

		# convert to certain decimal points
		current_units = float(data['available_'+self.currency.lower()])
		self.current_units = int(current_units*10000)/10000
		self.current_krw = float(data['available_krw'])


	def get_market_buy(self):
		response = self.call(path='/public/ticker/'+self.currency)
		return float(response['buy_price'])


	def get_market_sell(self):
		response = self.call(path='/public/ticker/'+self.currency)
		return float(response['sell_price'])


	def confirm_units(self, units, direction=False):
		from re import sub

		if True:
			if units=='*' and direction == 'buy':
				units = self.current_krw / self.get_market_sell()
			elif units=='*' and direction == 'sell':
				units = self.current_units

			units = int(float(sub(',','',str(units)))*10000)/10000
		else:
			raise UnitsError(units,direction)
		
		return units


	def buy_when(self, price, units, break_price=999999999999,
				success_callback=blank_callback, break_callback=blank_callback):
		from time import sleep

		prev_market_sell = 0
		price = self.confirm_units(price)

		while True:
			current_market_sell = self.get_market_sell()

			if current_market_sell <= price:
				units = self.confirm_units(units, direction='buy')
				while True:
					bid_call = self.call(path='/trade/market_buy',
									params={'currency':self.currency, 'units':units})
					if bid_call == False:
						units = self.confirm_units(units*0.9)
						continue
					break

				logging.info("\n[BID CALL COMPLETE]\n"+\
							"\tprice: {:,}\n".format(float(bid_call[0]['price']))+\
							"\tfee: {:,})\n".format(float(bid_call[0]['fee']))+\
							"\tunits: {:,}\n".format(float(bid_call[0]['units']))
							)
				self.update()
				success_callback()
				return

			if current_market_sell >= break_price:
				break_callback()
				return

			elif prev_market_sell != current_market_sell:
				logging.info('Current Market: {:,} | Bid Level: {:,}'.\
						format(current_market_sell, price))
				prev_market_sell = current_market_sell
	
			sleep(self.delay)


	def sell_when(self, price, units, break_price=0,
				success_callback=blank_callback, break_callback=blank_callback):
		from time import sleep

		prev_market_buy = 0
		price = self.confirm_units(price)

		while True:
			current_market_buy = self.get_market_buy()

			if current_market_buy >= self.confirm_units(price):
				while True:
					# prevent temporary error crashdown
					units = self.confirm_units(units, direction='sell')
					ask_call = self.call(path='/trade/market_sell',
									params={'currency':self.currency, 'units':units})
					if ask_call == False:
						continue

					logging.info("\n[ASK CALL COMPLETE]\n"+\
								"\tprice: {:,}\n".format(float(ask_call[0]['price']))+\
								"\tfee: {:,})\n".format(float(ask_call[0]['fee']))+\
								"\tunits: {:,}\n".format(float(ask_call[0]['units']))
								)
					break
				self.update()
				success_callback()
				return

			if current_market_buy <= break_price:
				break_callback()
				return

			elif prev_market_buy != current_market_buy:
				logging.info('Current Market: {:,} | Ask Level: {:,}'.\
							format(current_market_buy, price))
				prev_market_buy = current_market_buy
	
			sleep(self.delay)


	def convert_distance(self, distance):
		unit = {'s':1,'m':60,'h':3600,'d':3600*24}
		total_sec = float(distance[:-1])*unit[distance[-1]]
		return int(total_sec*100)/100


	def log(self):
		from time import sleep
		from os import makedirs, path
		from datetime import datetime
		from csv import writer

		PATH_NAME = './log/{}/'.format(self.currency)
		FILE_NAME = datetime.now().strftime(self.currency+"-%y-%m-%d.csv")

		if not path.exists(PATH_NAME): makedirs(PATH_NAME)

		while True:
			previous_data = None

			if path.exists(PATH_NAME+FILE_NAME):
				with open(PATH_NAME+FILE_NAME, 'r') as fp: previous_data = fp.read()
			
			fp = open(PATH_NAME+FILE_NAME, 'w')

			if previous_data: fp.write(previous_data)

			while True:
				writer(fp, delimiter=',').writerow(\
					[datetime.now().strftime('%y%m%d%H%M%S'),self.get_market_sell()])
				fp.flush()

				sleep(self.log_distance)

				NEW_NAME = self.currency+datetime.now().strftime("-%y-%m-%d.csv")
				if NEW_NAME != FILE_NAME:
					FILE_NAME = NEW_NAME
					break