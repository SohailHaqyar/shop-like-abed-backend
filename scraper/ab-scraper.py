import requests
from bs4 import BeautifulSoup
final_products = []

ab_base_url = 'https://www.killdeal.gr/prosfores-fylladia.aspx?sid=21&pn='
promitions_url_link = 'https://www.ab.gr/search/promotions?q=promotions:relevance:offers:true'


def get_data(page_number):
    products = []
    url = ab_base_url + str(page_number)
    data = requests.get(url)
    print('Going over Page: ', page_number)
    page = BeautifulSoup(data.text, 'html.parser')
    for product in page.find('ul', {'class': 'offers-list'}).find_all('li'):
        title = product.find('h2', {'class': 'product-name'})
        discount = product.find('label', {'class': 'promo-tag'})
        image_url = product.find('img').get('src')
        new_price = product.find('div', {'class': 'price'}).text
        old_price = product.find('div', {'class': 'deleted-price'}).text
        if old_price == '':
            old_price = 'None'
        if discount == None:
            discount_details = 'None'
        else:
            discount_details = discount.text

        if title is not None:
            products.append({
                'title': title.text.strip(),
                'discount_details': discount_details.strip(),
                'link': promitions_url_link.strip(),
                'label': '',
                'source': 'Ab',
                'image_url': image_url,
                'new_price': new_price.strip(),
                'old_price': old_price.strip()
            })
    final_products.extend(products)
    print(len(products))
    if len(products) > 0 and page_number < 5:
        get_data(page_number + 1)


get_data(0)
for offer in final_products:
    data = requests.post(
        'https://shop-like-abed.herokuapp.com/deals', data=offer)
    print(data.json())
