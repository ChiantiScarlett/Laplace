# CashCat


**CashCat** is a simple python-based cryptocurrency trading modules using Bithumb API.

### Usage

Under the same directory with [cashcat], make a example.py like this:
```python
# ./example.py

from cashcat import CashCat
token = {
	'key':'', # CONNECT_KEY from Bithumb API
	'secret': '', # SECRET_KEY from Bithumb API
	'currency': '' # ['BTC','ETH','DASH','LTC','ETC','XRP','BCH','XMR']
}

cat = CashCat(**token)
cat.buy_when(bid_price=14000, units='max')
```

### class CashCat:
```python
cat = CashCat(**token)
```

#### self.set_delay(delay :float)
```python
cat.set_delay(3)
```
- delay :: the delay time of self.buy_when() and self.sell_when(). Default value is 2.0.
- DO NOT set delay below 0.15 as private API Call is limited to 10 times in a second. 

#### self.get_market_buy()
```python
data = cat.get_market_buy()
```
- Returns float type of current market buy price(= ask price).

#### self.get_market_sell()
```python
data = cat.get_market_sell()
```
- Returns float type of current market sell price(= sell price).

#### self.current_krw
``` python
data = cat.current_krw
```

- Returns float type of current KRW.

#### self.current_units
``` python
data = cat.current_units
```

- Returns float type of current available units of the currency.


#### self.buy_when(bid_price , units, break_when, success_callback, break_callback)
```python
def buy_success(response):
	print("BID CALL COMPLETE : {}".format(response['price']))


cat.buy_when(bid_price=319400, units='max', success_callback=buy_success)
```
Check market price with delay. Necessary parameter: bid_price, units

- bid_price :: float type. If  current market price <= bid_price, buy the currency with written amount of units.
- units :: float type. Must be larger than 0.1. Can be 'max', which brings the maximum amount available.
- break_when :: float type. If break_when <= current market price, break the function.
- success_callback :: function type. It is a custom callback function that can be run after the purchase of currency. with the dict type parameter 'response'. The keys are the followings: 'cont_id',' fee', 'units', 'price', and 'total'.
- break_callback :: function type. A custom callback function that can be run when break_when <= current market price. Similar to success_callback, but have 'current_market_buy' and 'break_when' as the key of 'response' parameter.



#### self.sell_when(ask_price , units, break_when, success_callback, break_callback)
```python
def sell_success(response):
	print("ASK CALL COMPLETE : {}".format(response['price']))


cat.sell_when(ask_price=320400, units='max', success_callback=sell_success)
```
Check market price with delay. Necessary parameter: ask_price, units

- ask_price :: float type. If  current market price >= ask_price, sell the currency with written amount of units.
- units :: float type. Must be larger than 0.1. Can be 'max', which brings the maximum amount available.
- break_when :: float type. If current market price <= break_when, break the function.
- success_callback :: function type. It is a custom callback function that can be run after the sell of currency. with the dict type parameter 'response'. The keys are the followings: 'cont_id',' fee', 'units', 'price', and 'total'.
- break_callback :: function type. A custom callback function that can be run when current market price <= break_when. Similar to success_callback, but have 'current_market_buy' and 'break_when' as the key of 'response' parameter.
