import yfinance as yf
from datetime import datetime
import pandas as pd
import concurrent.futures
import threading
import requests
from bs4 import BeautifulSoup
import time

#stock = yf.Ticker(ticker)
#raw_info = stock.info
#stock_current = stock.info['currentPrice']

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
tables = pd.read_html(url)

# The first table contains the S&P 500 symbols
sp500_symbols = tables[0]['Symbol'].tolist()

data500 = []
lock = threading.Lock()  # Create a lock for thread safety

test = []


# THE STOCK STATTTTSSSS 
def show_this_market(symbol):
    stock = yf.Ticker(symbol)
    
    # Fetching the live price data
    live_price = stock.history(period="1d", interval="1m")


    
    try:
        current_price = live_price['Close'].iloc[-1]
        close_prices = live_price['Close'].tolist()
        datetime_list = live_price.index.tolist()



        
        # Formatting the output
        output = {"symbol": symbol, "prices":close_prices, "datetime": datetime_list}
        
        # Use lock to ensure thread-safe access to data500
        with lock:
            data500.append(output)
    
    except IndexError:
        print(f"Failed to retrieve price data for {symbol}.")
        
        
stock30 = []    
#STOCK FINDERRRRR    
def scrape_finviz_stocks():
    stock_symbols = []
    i = 1
    x = 122
    while i < x:
        if i == 1:
            i = ""
            
        url = f"https://finviz.com/screener.ashx?v=111&s=ta_mostvolatile&r={i}"  # Filter for high-volume stocks
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error fetching the page: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        # Try to find the table element
        table = soup.find("table", class_= 'styled-table-new is-rounded is-tabular-nums w-full screener_table')
        
        # If the table is not found, print the HTML to debug
        if table is None:
            print("Table not found! Printing page content for inspection:")
            print(soup.prettify())  # This will print the entire HTML of the page
            return []

        # Extract the stock symbols

        for row in table.find_all("tr")[1:]:  # Skip the header row
            symbol = row.find_all("td")[1].text
            stock_symbols.append(symbol)
            
        if i == "":
            i = 1
        
        i += 20

    return stock_symbols
    
    
from datetime import datetime


def stock_buy(symbol, new_price):
    for item in stock30:
        if item["symbol"] == symbol:
            item["buy_price"] = new_price
            item["Active"] = True
            item["peak_price"] = new_price
            print(f"BUY stock: {symbol}, price: {new_price}")
            return

    
def stock_sell(symbol, sell_price):
    for item in stock30:
        if item["symbol"] == symbol:
            item["sell_price"] = sell_price
            item["Active"] = False
            item["investment"] = (sell_price / item["buy_price"]) * item["investment"]
            item["low_price"] = sell_price
            
            print(f"SELL Stock: {item['symbol']}, Sell Price: {sell_price}, Investment: {item['investment']}")
            return   

def stock_maintainer_outer():
    for stock in stock30:
        symbol = stock["symbol"]
        datetime = stock["datetime"]
        current_price = stock["current_price"]
        previous_price = stock["previous_price"]
        buy_price = stock["buy_price"]
        sell_price = stock["sell_price"]
        peak_price = stock["peak_price"]
        low_price = stock["low_price"]
        profit_zone = stock["profit_zone"]
        Active = stock["Active"]
        opportunity_tracker = stock["oppotunity_tracker"]
        fails = stock["fails"]
        investment = stock["investment"]

        # Update peak and low prices
        stock["peak_price"] = max(current_price, peak_price)
        stock["low_price"] = min(current_price, low_price)

        if fails >= 5:
            # Stock has failed too many times, skip this iteration
            continue

        if not Active:  # If stock is not active (i.e., not currently held)
            # First buy of the day logic
            if sell_price == 0 and current_price > previous_price * 1.001:
                stock_buy(symbol, current_price)
                continue  # Proceed to next stock after buying

            # Rebuy logic if price meets or exceeds sell price
            if sell_price > 0 and current_price >= sell_price:
                stock_buy(symbol, current_price)
                continue  # Proceed after rebuying

            # Use opportunity tracker to buy on rising trend
            if opportunity_tracker and current_price >= low_price * 1.005:
                stock_buy(symbol, current_price)
                stock["opportunity_tracker"] = False  # Reset after buy
                stock["low_price"] = current_price  # Reset low price
                continue

        else:  # Stock is active (currently held)
            # Activate profit zone if price rises sufficiently above buy price
            if not profit_zone and current_price > buy_price * 1.003:
                stock["profit_zone"] = True

            # Sell if in profit zone and price drops from the peak
            if profit_zone and current_price < peak_price * 0.98:
                stock_sell(symbol, current_price)
                stock["opportunity_tracker"] = True
                continue

            # Stop loss condition: sell if price drops significantly
            if current_price <= buy_price * 0.975:
                stock_sell(symbol, current_price)
                stock["fails"] += 1
                continue

            # End of day selling condition
            if "15:59:00" in str(datetime):
                stock_sell(symbol, current_price)
                stock["fails"] = 2  # Slight penalty for end-of-day sale
                stock["profit_zone"] = False
                stock["opportunity_tracker"] = False
                print("END OF DAY SELL")
                continue


            
                
                
                


# Helper function to update stock details



                    
def stock30_add(symbol, price, date):
    
    output = {"symbol": symbol,
    "datetime": str(date),
    "current_price": price,
    "previous_price": price,
    "buy_price": 0,
    "sell_price": 0,
    "peak_price": price,
    "low_price": price,
    "profit_zone": False,
    "Active": False,
    "oppotunity_tracker": False,
    "fails": 0,
    "investment": 100,}
    
    stock30.append(output)
    
    
    
def update_stock30(name, new_price, date):
    for item in stock30:
        if item["symbol"] == name:
            item['previous_price'] = item['current_price']
            item['current_price'] = new_price
            
            item['datetime'] = date
            print(f"Updated stock: {name}, New price: {new_price}, Date: {date}")
            return  # Once found, no need to continue
            
    print(f"Stock {name} not found for update.")

        
                        
def update_or_add_stock(name, price, date):
    # Check if the item already exists
    found = False
    for item in stock30:
        if item["symbol"] == name:
            update_stock30(name, price, date)
            found = True
            break
    # If not found, add a new entry
    if not found:
        stock30_add(name, price, date)   
        

             
# Create and start threads
max_threads = 10
symbols = scrape_finviz_stocks()



# Using ThreadPoolExecutor to manage threads
with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    executor.map(show_this_market, symbols)  # Change the slice as needed
    

#print(len(data500))
testdata = data500[:30]



def convert_to_nested_pairs(input_list):
    result = []
    prices = [item['prices'] for item in input_list]
    names = [item['symbol'] for item in input_list]
    dates = [item['datetime'] for item in input_list]

    for i in range(max(len(prices_list) for prices_list in prices)):
        inner_list = []
        for j in range(len(input_list)):
            if i < len(prices[j]):
                inner_list.append({
                    "name": names[j],
                    "price": prices[j][i],
                    "date": dates[j][i]
                })
        result.append(inner_list)

    return result  

sorted_test = convert_to_nested_pairs(testdata)

for round in sorted_test:
    for stock in round:
# Each 'stock' is a dictionary within the 'round' list
        update_or_add_stock(stock["name"], stock["price"], stock["date"])
    stock_maintainer_outer()
    #time.sleep(2)
    

    
#for x in testdata:
       # for price, date in zip(x["prices"], x["datetime"]):
            #update_or_add_stock(x["symbol"], price, date)
            

amount = 0
for x in stock30:
    print(f"Symbol: {x["symbol"]} - Investment amount now: {x["investment"]}")
    amount += x["investment"]

profit = amount - len(testdata) * 100

print(f"from an of investment of {len(testdata) * 100} we gain {profit}%")

