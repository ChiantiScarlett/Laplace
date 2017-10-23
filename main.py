from laplace import Laplace

def main():
	SETTINGS_PATH = './settings.json'
	
	lp = Laplace(spath=SETTINGS_PATH)
	# lp.buy_when(price='228', units='*')
	# lp.sell_when(price='227', units='*')
	lp.log()

if __name__ == "__main__":
	main()