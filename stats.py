import api as polo
from coinmarketcap import Market
import ast
import json 
import time
from blessings import Terminal 
import apikey 
from retrying import retry 


# API Key, Secret
def getApiDetails():
	polo_key = apikey.my_polo_key
	polo_secret = apikey.my_polo_secret
	return polo_key, polo_secret

# Grab the key/secret pair from the apikey.py file 
polo_key, polo_secret = getApiDetails()

# Initialize 
pol = polo.poloniex(polo_key, polo_secret )
# This is for different colour outputs of text 
term = Terminal()

# Get ticker 
@retry(wait_exponential_multiplier=100, wait_exponential_max=1000)
def get_ticker():
	try:
		all_ticker = pol.returnTicker()
		return all_ticker
	except Exception as e: 
		print "Exception while Getting poloniex ticker: " + str(e)
		raise Exception("Retry!")

# Get BTC_USD rate from coinmarketcap
@retry(wait_exponential_multiplier=100, wait_exponential_max=1000)
def get_btc_usd():
	try:
		coinmarketcap = Market()
	except Exception as e:
		print "Exception at coinmarketcap: " + str(e) 
		raise Exception("Retry!")
	try: 
		btc_usd = (json.loads(coinmarketcap.ticker("bitcoin")))[0]["price_usd"]
		return btc_usd
	except Exception as e:
		print "Exception while parsing coinmarketcap Json: " + str(e)
# Get history of trades
@retry(wait_exponential_multiplier=100, wait_exponential_max=1000)
def get_history():
	try:
		start = 1494418332
		end = int(time.time())
		history = pol.returnTradeHistory("all",start, end )
		return history
	except Exception as e:
		print "Exception While Getting poloniex history: " + str(e)
		raise Exception("Retry!")

# Get currency balance
@retry(wait_exponential_multiplier=100, wait_exponential_max=1000)
def get_balance():
	try:
		total_balance = pol.returnBalances()
		return total_balance
	except Exception as e:
		print "Exception While Getting Balance: " + str(e)
		raise Exception("Retry!")


# Get the detailed Overview of any Currency Pair, currency_pair = ["BTC_STR"] = string list
def get_overview(currency_pair):
	all_ticker = get_ticker()
	btc_usd = get_btc_usd()
	history_main = get_history()
	net_profit = 0.0
	for cur in currency_pair:

		history = history_main[cur]
		currency_ticker = all_ticker[cur]
		purchase_price = float(history[0]['rate'])
		purchase_fee = float(history[0]['fee'])
		purchase_amount = float(history[0]['amount']) 
		purchase_cost = (purchase_price* (purchase_amount))
		purchase_real_amount = purchase_amount * (1-purchase_fee) 		
		average_cost = purchase_cost/(purchase_real_amount)
		current_price = currency_ticker['last']
		profit_btc = ((float(current_price)) - average_cost) * (purchase_real_amount)
		profit = float(profit_btc) * float(btc_usd)
		print term.bold_bright_blue_on_black("------------------------------------------{}--------------------------------------------")
		print "You invested {} BTC for {} {}/ at {} BTC/{}".format(purchase_cost, (purchase_real_amount), cur.split("_")[1],
																	   purchase_price,cur.split("_")[1])
		print "Your Purchase Price with fees: {} BTC".format(str(average_cost))
		print "Current_Price: " + str(current_price)
		net_profit += profit 
		
		if profit < 0:
		
			 
			print term.bold_bright_red_on_black('Loss                  {} BTC/{} USD'.format(profit_btc, profit))
		else:
					 

			print term.yellow('Profit                 {} BTC/{} USD'.format(profit_btc, profit))

	if net_profit < 0:
		print term.bold_bright_red_on_black('Net Loss                  {} USD'.format(net_profit))
	else:
		print term.yellow('Net Profit                 {} USD'.format(net_profit))
	print term.bold_bright_white_on_black("------------------------------------------{}--------------------------------------------")





def get_total_balance():
	total_balance = get_balance()
	balance_currency = []
	balance_amount = []
	for key in total_balance:
		if int(10000000000 *float(total_balance[key])) > 0:
			balance_currency.append(key)
			balance_amount.append(total_balance[key])
	return balance_currency, balance_amount


def main_program():
	currency, amount = get_total_balance()
	currency_pair = []
	for cur in currency:
		if cur != "BTC":
			pair = "BTC_" + str(cur)
			currency_pair.append(pair)
	while True:
		get_overview(currency_pair)




main_program()