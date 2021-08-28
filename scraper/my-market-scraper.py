import requests
from bs4 import BeautifulSoup


final_products = []


def get_data(pageNumber):
    products = []
    url = "https://eshop.mymarket.gr/offers?sort_by=popularity&items_per_page=40&page=" + \
        str(pageNumber)
    data = requests.get(url)
    print("Going over Page: " + str(pageNumber))
    page = BeautifulSoup(data.text, 'html.parser')
    for product in page.find_all('article', {'class': 'product'}):
        title = product.find('h3', {'class': 'product-title'}).text.strip()
        old_price = product.find(
            'span', {'class': 'original-price'})
        if old_price == None:
            final_old_price = 'None'
        else:
            final_old_price = old_price.text.strip()
        new_price = product.find('span', {'class': "final-price"}).text.strip()
        link = product.find('a', {'class': 'product-link'}).get('href')
        image_div = product.find('div', {'class': 'product-image'}).find('img')

        if image_div.get('data-lazyload-src') != None:
            image_url = image_div.get('data-lazyload-src')
        else:
            image_url = image_div.get('src')
        products.append({
            'image_url': image_url,
            'link': link,
            'new_price': new_price,
            'old_price': final_old_price,
            'title': title,
            'source': 'Mymarket',
            'discount_details': 'None',
            'label': '',
        })
    final_products.extend(products)
    if len(product) > 0 and pageNumber < 10:
        get_data(pageNumber + 1)


get_data(1)
for offer in final_products:
    print(len(final_products))
    data = requests.post(
        'https://shop-like-abed.herokuapp.com/deals', data=offer)
    print(data.json())
