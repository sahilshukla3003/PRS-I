import requests
from bs4 import BeautifulSoup

proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "https://10.10.1.10:1080",
}
url = "https://www.amazon.com/s?k=iphone&crid=3TXBHR2ONAGND&sprefix=iphon%2Caps%2C631&ref=nb_sb_noss_2"
url1 = "https://www.flipkart.com/search?q=iphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}
r = requests.get(url1,headers=HEADERS)

soup = BeautifulSoup(r.text,'html.parser')
# print(soup.prettify())
span = soup.find(class_ = "_4rR01T")
print(span)