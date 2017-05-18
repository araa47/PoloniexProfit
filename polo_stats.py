import polo 
from coinmarketcap import Market
import ast
import json 
import time
from blessings import Terminal 
import apikey 



# API Key, Secret
def getApiDetails():
	polo_key = apikey.my_polo_key
	polo_secret = apikey.my_polo_secret
	return polo_key, polo_secret

polo_key, polo_secret = getApiDetails()


# Initialize 
pol = polo.poloniex(polo_key, polo_secret )
term = Terminal()


def get_overview(currency_pair):
	all_ticker = pol.returnTicker()
	currency_ticker = all_ticker[currency_pair]
	coinmarketcap = Market()
	btc_usd =  (json.loads(coinmarketcap.ticker("bitcoin")))[0]["price_usd"]

	history = pol.returnTradeHistory(currency_pair)
	if len(history) >=1:
		purchase_price = float(history[0]['rate'])
		purchase_amount = float(history[0]['amount'])
		purchase_fee = float(history[0]['fee'])
		purchase_total = purchase_fee + (purchase_price* purchase_amount)
	else:
		print history
	average_cost = purchase_total/(purchase_amount)
	current_price = currency_ticker['last']
#	current_price = 20
	profit_btc = ((float(current_price)) - average_cost) * purchase_amount
	profit = float(profit_btc) * float(btc_usd)
	print term.bold_bright_blue_on_black("------------------------------------------{}--------------------------------------------")
	print "You invested {} BTC for {} {}/ at {} BTC/{}".format(purchase_total, purchase_amount, currency_pair.split("_")[1],
																   purchase_price,currency_pair.split("_")[1])
	print "Your Purchase Price with fees: {} BTC".format(str(round(average_cost,8)))
	print "Current_Price: " + str(current_price)

	#print "PROFIT USD: " + str(profit) 
	if profit < 0:
			#       .bold_bright_red_on_black('Bright red on black')
			 #       print utils.bcolors.RED,
		 
		print term.bold_bright_red_on_black('Loss                  {} BTC/{} USD'.format(profit_btc, profit))
	else:
				   # print utils.bcolors.GREEN,

		print term.yellow('Profit                 {} BTC/{} USD'.format(profit_btc, profit))
			  

def get_balance():
	total_balance = pol.returnBalances()
	balance_currency = []
	balance_amount = []
	for key in total_balance:
		if int(100000*float(total_balance[key])) > 0:
			balance_currency.append(key)
			balance_amount.append(total_balance[key])
	return balance_currency, balance_amount

for i in range(10000000):
	get_overview("BTC_STR")
#	get_overview("BTC_LT")
	time.sleep(1)

#hist = pol.returnTradeHistory("BTC_ETH")
#print hist
'''
				print "You invested {} BTC for {} {}/{} BTC".format(btc_sum, ticker_sum, ticker.split("_")[1],
																   current_btc_sum)
			   # print "If you sold it all at the current price (assuming enough sell orders)"
		   #     print "BTC SUM" + str(btc_sum)
			#    print "AMount" + str(ticker_sum)
				print "Your Purchase Price with fees:       {} BTC".format(btc_sum/float(ticker_sum))
				print "Current Price without fees:          {} BTC".format(current_price_to_btc)

				if total_btc < 0:
			#       .bold_bright_red_on_black('Bright red on black')
			 #       print utils.bcolors.RED,
		 
					print term.bold_bright_red_on_black('Loss                  {} BTC/{} USD'.format(total_btc, total_usd))
				else:
				   # print utils.bcolors.GREEN,

					print term.yellow('Profit                 {} BTC/{} USD'.format(total_btc, total_usd))
				total_profit += total_usd    
				'''