from laplace import Laplace

def main():
	SETTINGS_PATH = './settings.json'
	
	lp = Laplace(spath=SETTINGS_PATH)
	# lp.buy_when(price='6,570,000', units='*')
	# lp.sell_when(price='6,700,000', units='*')
	lp.log()

if __name__ == "__main__":
	main()