class CurrencyError(Exception):
	def __init__(self, currency):
		self.currency = currency

	def __str__(self):
		return 'invalid currency: {}.'.format(self.currency)


class DelayError(Exception):
	def __init__(self, delay):
		self.delay = delay

	def __str__(self):
		return 'invalid delay: {}. (delay >= 0.18)'.format(self.delay)

class UnitsError(Exception):
	def __init__(self, units):
		self.units = units

	def __str__(self):
		return 'invalid units: {}.'.format(self.units)