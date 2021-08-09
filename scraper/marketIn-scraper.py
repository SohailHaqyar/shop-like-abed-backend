import requests
from bs4 import BeautifulSoup
import json
import random


final_products = []


def get_data(pageNumber):
    products = []
    url = "https://www.market-in.gr/el-gr/ALL/eidikh-prosfora?pageno=" + \
        str(pageNumber)
    data = requests.get(url)
    page = BeautifulSoup(data.text, 'html.parser')
    for product in page.find_all('div', {'class': 'product-col'}):
        a = product.find('a', {'class': 'product-thumb'})
        old_price = product.find('span', {'class': 'old-price'})
        if old_price != None:
            link = a.get('href')
            image = a.find('img').get('src')
            title = product.find('a', {'class': 'product-ttl'}).text
            new_price = product.find('span', {'class': 'new-price'}).text
            label = product.find('a', {'class', 'product-brand'}).text
            discount_percentage = product.find(
                'span', {'class': "disc-value"}).text
            products.append({
                "link": link,
                "image_url": image,
                "label": label,
                "title": title.strip(),
                "old_price": old_price.text,
                "new_price": new_price,
                "discount_details": discount_percentage
            })
    final_products.extend(products)
    if len(products) != 0:
        get_data(pageNumber+1)


get_data(1)

for offer in final_products:
    data = requests.post(
        'https://shop-like-abed.herokuapp.com/deals', data=offer)
    print(data.json())


# random_number = random.randint(1, 200)
# with open(f'/tmp/data{random_number}.json', 'w',) as file:
#    json.dump(final_products, file, ensure_ascii=False)
