class Tracer:
	def __init__(self, master):
		self.currency = master.currency
		self.data_range = master.trace_days

	def trace(self):
		from scipy import stats
		import numpy as np
		import pandas as pd
		from datetime import datetime
		from os import listdir

		DIR_PATH = './log/{}/'.format(self.currency)
		LATEST_FILE = self.currency+datetime.now().strftime("-%y-%m-%d.csv")
		files = listdir(DIR_PATH)

		while len(files):
			pass

		pd.read_csv()

		x = np.random.random(10)
		y = np.random.random(10)
		alpha, beta, r_val, p_val, std_err =\
			stats.linregress(x,y)

		# working on the function

