class Laplace:
	# caller
	def __init__(self, **kwargs):
		from modules.bithumb_api import XCoinAPI

		self.core = XCoinAPI(kwargs['key'], kwargs['secret'])
		self.unit = 0
		self.krw = 0

		self.update()


	def call(self, path, rgParams={}):
		response = self.core.xcoinApiCall(path, rgParams)
		return response


	def update(self):
		response = self.call(path='/info/balance')
		print(response)