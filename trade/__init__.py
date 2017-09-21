from cashcat.auth import XCoinAPI
from cashcat.error import CurrencyError, DelayError, UnitsError
from time import sleep
import logging

def empty_callback(response):
	pass


class CashCat:
	def __init__(self, key, secret, currency):
		self.core = XCoinAPI(key, secret)
		self.currency = currency

		self.delay = 2
		self.current_krw = None
		self.current_units = None

		# check currency:
		if str(self.currency).upper() not in ['BTC','ETH','DASH','LTC','ETC','XRP','BCH','XMR']:
			raise CurrencyError

		self.update()

	def update(self):
	# update current krw and units
		data = self.safe_call(\
			path='/info/balance/',params={'currency': self.currency})

		current_units = float(data['available_'+self.currency.lower()])
		current_units = int(current_units*10000)/10000

		current_krw = float(data['available_krw'])

		self.current_units = current_units
		self.current_krw = current_krw


	def safe_call(self, path, params={}):
	# call and get data from Bithumb
		while True:
			logging.debug("safe_call request to: {}, {}".format(path, str(params)))
			response = self.core.xcoinApiCall(path, params)
			logging.debug("safe_call response: {}".format(str(response)))

			if response['status'] != '0000':
				logging.critical(str(response))

				logging.critical("re-call in 1.2 sec.")
				sleep(1.2)
				continue
			
			else:
				return response['data']
			
			break

	def get_market_buy(self):
	# returns current market-buy price
		response = self.safe_call(path='/public/ticker/'+self.currency)
		return float(response['buy_price'])

	def get_market_sell(self):
	# returns current market-sell price
		response = self.safe_call(path='/public/ticker/'+self.currency)
		return float(response['sell_price'])

	def purify_units(self, units, direction=False):
	# gets unit and round down to 4 digit below decimal point.

		if direction:
			if direction == 'buy' and str(units).upper() == 'MAX':
				# get maximum units you can buy
				units = self.current_krw / self.get_market_sell()
			elif direction == 'sell' and str(units).upper() == 'MAX':
				# get maximum units you can sell
				units = self.current_units

			# if type(units) == float, then skip.
			try:
				float(units)
			except:
				raise UnitsError(units)

		# check if type == str in try-except clause
		try:
			units = int(float(units)*10000)/10000
			return units

		except:
			raise UnitsError(units)

	def set_delay(self, delay):
		try:
			float(delay) # prevent string
			if delay < 0.15:
				raise DelayError
		except:
			raise DelayError

		self.delay = delay


	def buy_when(self, bid_price, units, break_when=False,
		success_callback=empty_callback, break_callback=empty_callback):
	# buy when the market price meets the bid_price
	# Returns True when successfully bought the currency
	# Returns False when the market price met break_when value

		# check units if it is not invalid.
		units = self.purify_units(units, direction='buy')
		
		prev_market_sell = 0			
		while True:
			current_market_buy = self.get_market_sell()
			if current_market_buy <= bid_price:
			# Buy if current price goes below bid_price

				# get newest units ( because appropriate max units
				# for bid call is calcualted by the real-time market price )
				units = self.purify_units(units)

				# bid call
				bid_call = self.safe_call(path='/trade/market_buy',
							params={'currency':self.currency, 'units':units})
				
				logging.info("\n[BID CALL COMPLETE]\n"+\
								"\tprice: {:,}\n".format(float(bid_call[0]['price']))+\
								"\tfee: {:,})\n".format(float(bid_call[0]['fee']))+\
								"\tunits: {:,}\n".format(float(bid_call[0]['units']))
							)
				
				self.update()
				success_callback(response=bid_call[0])
				return

			if break_when:
			# Break if current price goes above break_when
				if break_when <= current_market_buy:
					break_callback(response={
						'current_market_buy':current_market_buy,
						'break_when':break_when})
					return

			else:
			# Otherwise give delay and redo the process
				if prev_market_sell != current_market_buy:
					logging.info('Current Market: {:,} | Bid Level: {:,}'.format(current_market_buy, bid_price))
					prev_market_sell = current_market_buy
				sleep(self.delay)




	def sell_when(self, ask_price, units, break_when=False,
		success_callback=empty_callback, break_callback=empty_callback):
	# sell when the market price meets the ask_price
	# Returns True when successfully sold the currency
	# Returns False when the market price met break_when value

		# check units if it is not invalid.
		units = self.purify_units(units, direction='sell')
		
		prev_market_sell = 0			
		while True:
			current_market_sell = self.get_market_buy()
			if current_market_sell >= ask_price:
			# Buy if current price goes above ask_price

				# ask call
				ask_call = self.safe_call(path='/trade/market_sell',
							params={'currency':self.currency, 'units':units})
				
				logging.info("\n[ASK CALL COMPLETE]\n"+\
								"\tprice: {:,}\n".format(float(ask_call[0]['price']))+\
								"\tfee: {:,})\n".format(float(ask_call[0]['fee']))+\
								"\tunits: {:,} \n".format(float(ask_call[0]['units']))
							)

				self.update()
				success_callback(response=ask_call[0])
				return

			if break_when:
			# Break if current price goes below break_when
				if break_when >= current_market_sell:
					break_callback(response={
						'current_market_sell':current_market_sell,
						'break_when':break_when})
					return

			else:
			# Otherwise give delay and redo the process
				if prev_market_sell != current_market_sell:
					logging.info('Current Market: {:,} | Ask Level: {:,}'.format(current_market_sell, ask_price))
					prev_market_sell = current_market_sell
				sleep(self.delay)