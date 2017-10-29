from modules.core import Laplace

SETTINGS = {
	"key": "",
	"secret": "",
	"currency": "BTC",
	"delay":1.5,
	"log_distance": 600,
	"trace_days": 2
	}

def main():	
	lp = Laplace(**SETTINGS)
	# lp.buy_when(price='6,570,000', units='*')
	# lp.sell_when(price='6,700,000', units='*')
	# lp.log()


if __name__ == "__main__":
	main()