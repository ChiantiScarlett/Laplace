class NoSettingsPathError(Exception):
	def __init__(self, spath):
		self.spath = spath

	def __str__(self):
		return 'Cannot find spath file: "{}".'.format(self.spath)

class InvalidSettingsPathKeyError(Exception):
	def __init__(self, spath_keyset):
		self.spath_keyset = spath_keyset

	def __str__(self):
		return 'keys should be {}.'.format(self.spath_keyset)


class ResponseError(Exception):
	def __init__(self, code, error_str):
		self.code = code
		self.error_str = error_str

	def __str__(self):
		return "[{}] {}".format(self.code, self.error_str)


class UnitsError(Exception):
	def __init__(self, units, direction):
		self.units = units
		self.direction = direction

	def __str__(self):
		return "[direction:{}] {}".format(self.direction, self.units)

class TraceDaysError(Exception):
	def __init__(self):
		pass

	def __str__(self):
		return "trace_days should be an integer (>= 1)."