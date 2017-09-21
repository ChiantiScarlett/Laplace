from cashcat.error import ParameterError
from cashcat.auth import XCoinAPI
import logging
import os, json
from shutil import rmtree
from time import sleep
from datetime import datetime
from threading import Thread


class Tracer:
	def __init__(self, key, secret, currency):
		self.core = XCoinAPI(key, secret)
		self.currency = currency.upper()

		# check currency:
		if str(self.currency).upper() not in ['BTC','ETH','DASH','LTC','ETC','XRP','BCH','XMR']:
			raise CurrencyError


	def trace(self, hold='1d', stamp='15m', daemon=True):
		m_table = {'s':1,'m':60,'h':3600,'d':3600*24,'w':3600*24*7}

		# convert measurement into seconds
		hold = m_table[hold[-1]]*float(hold[:-1])
		stamp = m_table[stamp[-1]]*float(stamp[:-1])

		hold_cnt = int(hold/stamp)

		trace_thread = Thread(
				target=self.start_trace,
				kwargs={'hold_cnt':hold_cnt,'stamp':stamp})
		trace_thread.setDaemon(daemon)
		trace_thread.start()


	def start_trace(self, hold_cnt, stamp):

		# create new dir '__cc_cache__', and make empty json.
		if os.path.exists('__cc_cache__'): rmtree('__cc_cache__')
		os.mkdir('__cc_cache__')

		with open("__cc_cache__/tracer.trace.json" ,'w') as fp:
			fp.write(json.dumps({'data':[]}))
		
		while True:
		# Write data::
			with open("__cc_cache__/tracer.trace.json", 'r') as fp:
				stamp_list = json.loads(fp.read())['data']
			
			# add (timestamp, sell_price)
			stamp_list.append(self.get_data())
			
			# if it reaches maximum limit(hold_cnt), then pop previous data
			if len(stamp_list) > hold_cnt: stamp_list.pop(0)
			
			# save
			with open("__cc_cache__/tracer.trace.json", 'w') as fp:
				json.dump({'data':stamp_list}, fp)

			# sleep for stamp delay
			sleep(stamp)

	def get_data(self):
	# call and get data from Bithumb
		while True:
			logging.debug("safe_call request to: /public/ticker/"+self.currency.lower())
			response = self.core.xcoinApiCall('/public/ticker/'+self.currency.lower(), {})
			logging.debug("safe_call response: {}".format(str(response)))

			if response['status'] != '0000':
				logging.info(str(response))

				logging.critical("re-call in 1.2 sec.")
				sleep(1.2)
				continue
			
			else:
				break
		
		# timestamp:yymmddHHMMSS, where:
		# [y:year, m:month, d:day, H:hour,M:minute,S:second]
		timestamp = datetime.now().strftime("%y%m%d%H%M%S")
		sell_price= response['data']['sell_price']

		return (timestamp, sell_price)



# if param not in ['hour','day','week','month','year']:
# 	return ParameterError(param)
# data = json.loads(urlopen('https://api.lionshare.capital/api/prices?period='+param).read().decode('utf-8'))['data']
# print(data[self.currency])


# from time import sleep
# from threading import Thread

# def t1():
# 	while True:
# 		print("t1")
# 		sleep(1)

# def t2():
# 	while True:
# 		print("t2")
# 		sleep(1.7)

# ta = Thread(target=t1,args=())
# # ta.setDaemon(True)
# ta.start()

# tb = Thread(target=t2,args=())
# # tb.setDaemon(True)
# tb.start()