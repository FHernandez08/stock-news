import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "+18554975395"
VERIFIED_NUMBER = "+18326403493"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# API Keys
NEWS_API = "f93df7b596464c09984c2c1f286238b4"
STOCK_API = "YCTYNO9FX0BGK80K1"
TWILIO_SID = "AC747d089a02d32d9d771f5ffc2838dc4c"
TWILIO_AUTH_TOKEN = "fd83c67df9348a60e5d9b94bf41e3f2d"

STOCK_FUNCTION = "TIME_SERIES_DAILY"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_params = {
    "function": STOCK_FUNCTION,
    "symbol": STOCK_NAME,
    "apikey": STOCK_API
}

stock_response = requests.get(STOCK_ENDPOINT, stock_params)
data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = (difference / float(yesterday_closing_price)) * 100
print(diff_percent)

## STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if diff_percent > 1:
    news_params = {
        "apiKey": NEWS_API,
        "qInTitle":COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    print(articles)

    three_articles = articles[:3]
    print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)


    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )


