import requests
import json
from bs4 import BeautifulSoup


page1_data = requests.get(
    'https://www.market-in.gr/el-gr/ALL/eidikh-prosfora?pageno=1')

page2_data = requests.get(
    'https://www.market-in.gr/el-gr/ALL/eidikh-prosfora?pageno=2'
)
page1 = BeautifulSoup(page1_data.text, 'html.parser')
page2 = BeautifulSoup(page2_data.text, 'html.parser')
products = []
for product in page1.find_all('div', {'class': 'product-col'}):
    a = product.find('a', {'class': 'product-thumb'})
    link = a.get('href')
    image = a.find('img').get('src')
    title = product.find('a', {'class': 'product-ttl'}).text
    old_price = product.find('span', {'class': 'old-price'}).text
    new_price = product.find('span', {'class': 'new-price'}).text
    discount_percentage = product.find('span', {'class': "disc-value"}).text
    products.append({
        "link": link,
        "image_url": image,
        "title": title.strip(),
        "old_price": old_price,
        "new_price": new_price,
        "discount_details": discount_percentage
    })

for product in page2.find_all('div', {'class': 'product-col'}):
    a = product.find('a', {'class': 'product-thumb'})
    old_price = product.find('span', {'class': 'old-price'})
    if old_price != None:
        link = a.get('href')
        image = a.find('img').get('src')
        title = product.find('a', {'class': 'product-ttl'}).text
        new_price = product.find('span', {'class': 'new-price'}).text
        discount_percentage = product.find(
            'span', {'class': "disc-value"}).text
        products.append({
            "link": link,
            "image_url": image,
            "title": title.strip(),
            "old_price": old_price.text,
            "new_price": new_price,
            "discount_details": discount_percentage
        })


for offer in products:
    data = requests.post('http://localhost:3000/deals', data=offer)
    print(data.json())
