import requests
from twilio.rest import Client

COMPANY_NAME = "Tesla Inc"
api_stock = "" # Deleted before uploading

parameters_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": api_stock
}

response = requests.get("https://www.alphavantage.co/query", params=parameters_stock)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_close = float(data_list[0]["4. close"])
daybefore_close = float(data_list[1]["4. close"])

if (yesterday_close/daybefore_close)-1 > 0.04:
    symbol = "△"
elif (yesterday_close/daybefore_close)-1 < -0.04:
    symbol = "▽"
percent = round(abs((yesterday_close/daybefore_close)-1))*100

api_news = "" # Deleted before uploading
parameters_news = {
    "q": "tesla",
    "from": "2024-03-02",
    "sortBy": "publishedAt",
    "apiKey": api_news
}

response_news = requests.get("https://newsapi.org/v2/everything", params=parameters_news)
response_news.raise_for_status()
news = response_news.json()

account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)

for i in range(3):
    message = client.messages \
        .create(
        body=f"TSLA: {symbol}{percent}%"
             f"\nTitle: {news["articles"][i]["title"]}, "
             f"\nDescription: {news["articles"][i]["description"]}",
                from_="+150", to="+1682")


