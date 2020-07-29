import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options

def url_finder(user_input):
    # Options() hides the GUI of chrome and does everything in the background
    options = Options()
    options.add_argument('--headless')
    # options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    browser = webdriver.Chrome('./chromedriver', options=options)
    browser.get('https://www.google.com/')
    search_input = browser.find_element_by_css_selector('.gLFyf')
    search_input.clear()
    search_input.send_keys(f'{user_input} moneycontrol')
    time.sleep(1)
    search_input.send_keys(Keys.ESCAPE)
    lucky_btn = browser.find_elements_by_name('btnI')
    lucky_btn[1].click()
    output_url = browser.current_url
    return output_url


stocks = {
    'yesbank': 'https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/yesbank/YB',
    'vedanta': 'https://www.moneycontrol.com/india/stockpricequote/miningminerals/vedanta/SG',
    'vodafoneidea': 'https://www.moneycontrol.com/india/stockpricequote/telecommunications-service/vodafoneidealimited/IC8'
}
print('Stored stock options are: ')
stock_list = stocks.keys()
print('\n'.join(stock_list).upper())

stock_to_check = str(input('Please input stock name here : ').lower() or next(iter(stocks)))
# Response Variable with URL to grab data from
if stock_to_check in stock_list:
        res = requests.get(stocks.get(stock_to_check))

else:
    res = requests.get(url_finder(f'{stock_to_check}'))
# String text of HTML data
data = res.text
# to parse html to object, soup object
soup = BeautifulSoup(data, 'html.parser')
# to select particular class under <div>
nse_box = soup.select('div.nsedata_bx')

rates_list = []
print("_"*len(stock_to_check))
print(stock_to_check.upper())
print("_"*len(stock_to_check))
for i in nse_box:
    if i.select('.span_price_wrap'): rates_list.extend(i.select('.span_price_wrap'))
    if i.select('.priceprevclose'): rates_list.extend(i.select('.priceprevclose'))
    if i.select('.priceopen'): rates_list.extend(i.select('.priceopen'))
    if i.select(".todays_lowhigh_wrap"):
        for j_index, j in enumerate(i.select('.todays_lowhigh_wrap')):
            if j.select(".low_high1"): rates_list.extend(j.select('.low_high1'))
            if j.select(".low_high3"): rates_list.extend(j.select('.low_high3'))

for raw_string in rates_list:
    # to only pick the price value from the data string
    regex = r">(\d+.\d+)<"
    for i in re.finditer(regex, str(raw_string)):
        if 'span_price_wrap' in str(raw_string): last_traded_price = i.group(1)
        if 'priceprevclose' in str(raw_string): prev_close_price = i.group(1)
        if 'priceopen' in str(raw_string): open_price = i.group(1)
        if 'low_high1' in str(raw_string): low_price = i.group(1)
        if 'low_high3' in str(raw_string): high_price = i.group(1)

print(f"LAST TRADED PRICE : {last_traded_price}")
print(f"PREV CLOSING PRICE : {prev_close_price}")
print(f"OPEN PRICE : {open_price}")
print(f"TODAY'S LOW : {low_price}")
print(f"TODAY'S HIGH : {high_price}")

if last_traded_price > open_price:
    print('Green Candle')
    if open_price == low_price and last_traded_price == high_price:
        print(f'Bullish Marubuzo ! Open season for buying. Set stop loss at {low_price}.')



if last_traded_price < open_price:
    print('Red Candle')
    if open_price == high_price and last_traded_price == low_price:
        print(f'Bearish Marubuzo ! Open season for shorting. Set stop loss at {high_price}')

