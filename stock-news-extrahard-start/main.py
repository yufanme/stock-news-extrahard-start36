import requests
import datetime as dt
from newsapi import NewsApiClient

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

AV_API_KEY = "QJBEJGRF3O7UTNUK"
ALPHA_VANTAGE_END_POINT = "https://www.alphavantage.co/query"

NEWS_API_END_POINT = "https://newsapi.org/v2/everything"
NEWSAPI_API_KEY = "1aa76e5062a14bb3a6307d205d8ab3c5"

headers = {
          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/65.0.3325.181 Safari/537.36"
      }
proxies = {
    "https": "https://164.70.118.39:3128",
    "http": "http://59.21.84.108:80",
}

# # STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
alpha_vantage_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": AV_API_KEY
}
response = requests.get(ALPHA_VANTAGE_END_POINT, params=alpha_vantage_params)
response.raise_for_status()
alpha_vantage_data = response.json()

now = dt.datetime.now()
day = now.day
if day < 10:
    day = f"0{day}"
month = now.month
if month < 10:
    month = f"0{month}"
year = now.year

yesterday = f"{year}-{month}-{day -1}"
day_before_yesterday = f"{year}-{month}-{day -2}"

yesterday_price = float(alpha_vantage_data["Time Series (Daily)"][yesterday]["4. close"])
day_before_yesterday_price = float(alpha_vantage_data["Time Series (Daily)"][day_before_yesterday]["4. close"])
price_change = (yesterday_price-day_before_yesterday_price)/day_before_yesterday_price * 100
price_change = abs(price_change)
if price_change > 5:
    print("get news.")
else:
    print("change is too small.")


# # STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
# newsapi = NewsApiClient(api_key=NEWSAPI_API_KEY)
# all_articles = newsapi.get_everything(
#     q="Tesla",
#     sources='bbc-news,the-verge',
#     domains='bbc.co.uk,techcrunch.com',
#     from_param=f'{day_before_yesterday}',
#     to=f'{yesterday}',
#     language='en',
#     sort_by='relevancy',
#     page=2)
#
# response = newsapi.get_sources()
# print(response)
# print("end")

newsapi_params = {
    "apiKey": NEWSAPI_API_KEY,
    "qInTitle": COMPANY_NAME,
}
# response = requests.get(NEWS_API_END_POINT, params=newsapi_params)
response = requests.get(NEWS_API_END_POINT, params=newsapi_params)
response.raise_for_status()
news = response.json()

print(response.status_code)

# # STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

