import requests
import datetime as dt

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_API_KEY = "X6BB9IHVMM8BV7XD"
today = dt.datetime.now().date()
print(today)
yesterday = dt.datetime.now().date() - dt.timedelta(days=1)

news_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": NEWS_API_KEY
}


news_response = requests.get("https://www.alphavantage.co/query", params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()

no_info_yesterday = True

# today_close = float(news_response.json()["Time Series (Daily)"][f"{today}"]["1. open"])
yesterday_close = float(news_response.json()["Time Series (Daily)"][f"{yesterday}"]["1. open"])
n = 0
while no_info_yesterday:
    try:
        n += 1
        today_close = float(news_response.json()["Time Series (Daily)"][f"{today}"]["1. open"])
    except KeyError:
        today = dt.datetime.now().date() - dt.timedelta(days=1)
    else:
        no_info_yesterday = False

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

