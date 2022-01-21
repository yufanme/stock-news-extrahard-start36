import requests
import datetime as dt
from twilio.rest import Client
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
CHANGE = 0

ALPHA_VANTAGE_API_KEY = "QJBEJGRF3O7UTNUK"
ALPHA_VANTAGE_END_POINT = "https://www.alphavantage.co/query"

NEWS_API_END_POINT = "https://newsapi.org/v2/everything"
NEWSAPI_API_KEY = "1aa76e5062a14bb3a6307d205d8ab3c5"

account_sid = "AC8a95a85cabd382f190b3ac17e0a97d26"
auth_token = "1c531beaff38baf0e0b5b5148a225b61"

EMAIL = "562937707@qq.com"
PASSWORD = "bpyjiqjylklcbdhe"

# # STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
alpha_vantage_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": ALPHA_VANTAGE_API_KEY
}
response = requests.get(ALPHA_VANTAGE_END_POINT, params=alpha_vantage_params)
response.raise_for_status()
alpha_vantage_data = response.json()["Time Series (Daily)"]
print(alpha_vantage_data)
alpha_vantage_data_list = [value for (key, value) in alpha_vantage_data.items()]
yesterday = alpha_vantage_data_list[0]
day_before_yesterday = alpha_vantage_data_list[1]
yesterday_price = float(yesterday["4. close"])
print(yesterday_price)
day_before_yesterday_price = float(day_before_yesterday["4. close"])
print(day_before_yesterday_price)
price_change = (yesterday_price-day_before_yesterday_price)/day_before_yesterday_price * 100
print(price_change)
if price_change > 0:
    sign = "up"
else:
    sign = "down"

price_change = round(price_change, 2)
if abs(price_change) > CHANGE:
    print("send news")
    # # STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

    newsapi_params = {
        "apiKey": NEWSAPI_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    response = requests.get(NEWS_API_END_POINT, params=newsapi_params)
    response.raise_for_status()
    news = response.json()

    articles = response.json()
    three_articles = articles["articles"][:3]
    formatted_articles = f"TSLA: {sign}{price_change}%\n"
    for article in three_articles:
        formatted_articles += f"Headline: {article['title']}\n"
        formatted_articles += f"Brief: {article['description']}\n"
    print(formatted_articles)
    # # STEP 3: Use https://www.twilio.com
    # Send a separate message with the percentage change and each article's title and description to your phone number.
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body=f"{formatted_articles}",
            from_='+16065540848',
            to='+8619808145773'
        )
    print(message.status)

    with smtplib.SMTP("smtp.qq.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL,
                            to_addrs=EMAIL,
                            msg=f"Subject:STOCK NEWS\n\n{formatted_articles}")
else:
    print("change is too small.")


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

