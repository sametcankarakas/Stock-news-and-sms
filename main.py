import os
import requests
import datetime as dt
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = os.environ['STOCK_API_KEY']
NEWS_API_KEY = os.environ['NEWS_API_KEY']
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
assign_today = True
assign_yesterday = True

today = dt.datetime.now().date()
yesterday = dt.datetime.now().date() - dt.timedelta(days=1)

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
news_parameters = {
    "apiKey": NEWS_API_KEY,
    "qInTitle": COMPANY_NAME,
    "language": "en",
}

stock_response = requests.get("https://www.alphavantage.co/query", params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()
stock_name = stock_data["Meta Data"]["2. Symbol"]
print(stock_data)
print(stock_name)

# today_close = float(stock_data["Time Series (Daily)"][f"{today}"]["1. open"])
# yesterday_close = float(stock_data["Time Series (Daily)"][f"{yesterday}"]["1. open"])

# loop that assign open exchange days and before the day.(cuz somedays like weekends exchange offices closed.)
# Therefore to calculate yesterday or calculate today(if script runs everyday) it search open days in json data.
while assign_today:
    try:
        # if cannot find data in that day while we requested.Gives Key error...
        today_close = float(stock_data["Time Series (Daily)"][f"{today}"]["1. open"])
    except KeyError:
        # in here we going the day before and assign to varible to check data up there...
        today = dt.datetime.now().date() - dt.timedelta(days=1)
    else:
        yesterday_close = today_close
        if today_close == yesterday_close:
            yesterday = yesterday - dt.timedelta(days=1)
            while assign_yesterday:
                try:
                    # if cannot find data in that day while we requested.Gives Key error...
                    yesterday_close = float(stock_data["Time Series (Daily)"][f"{yesterday}"]["1. open"])
                except KeyError:
                    # in here we going the day before and assign to varible to check data up there...
                    yesterday = yesterday - dt.timedelta(days=1)
                else:
                    assign_yesterday = False
        assign_today = False
print(today, ": $", today_close)
print(yesterday, ": $", yesterday_close)

# calculates percentage between 2 days
percentage_result = (today_close / yesterday_close) * 100 - 100
# f"{percentage_result: .2f}" stand for two digits after comma...
print(f"{stock_name} stocks have been %", f"{percentage_result: .2f}", " changed")

if percentage_result >= 5 or percentage_result <= -5:
    news_response = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    for news in news_data[:3]:
        news_title = news["title"]
        news_brief = news["description"]
        message = client.messages.create(
            body=f"{STOCK} {percentage_result: .2f}??.\nTitle: {news_title}\nBrief: {news_brief}",
            from_="+18043748512",
            to="+905375167270"
        )
        print(news_brief)
        print(message.sid)
        print(message.status)

    # message = client.messages.create(
    #     to="+905375167270",
    #     from_="+18043748512",
    #     body=f"{STOCK} {percentage_result: .2f}??.\n{news_title}\n{news_brief}")
    # print(news_brief)
    # print(message.sid)
    # print(message.status)

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: ????2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: ????5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
