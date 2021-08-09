import requests
from bs4 import BeautifulSoup


final_products = []


lidl_product_base_url = 'https://www.lidl-hellas.gr'


def get_data():
    products = []
    url = "https://www.lidl-hellas.gr/oi-prosphorhes-mas"
    data = requests.get(url)
    page = BeautifulSoup(data.text, 'html.parser')
    for product in page.find_all('div', {'class': 'col'}):
        title = product.find('h3', {'class': 'product__title'})
        discount_details = product.find(
            'div', {'class': 'pricebox__highlight'})
        new_price = product.find('span', {'class', 'pricebox__price'})
        link = product.find('a', {'class', 'product__body'})
        image = product.find('img')
        old_price = product.find(
            'span', {'class': "pricebox__recommended-retail-price"})
        if title != None and discount_details != None and new_price != None and link != None:
            if old_price != None:
                final_old_price = old_price.text.split('\n')[1].strip()
            else:
                final_old_price = 'None'
            products.append({
                "link": lidl_product_base_url + link.get("href"),
                "image_url": image.get('src'),
                "title": title.text.strip(),
                "old_price": final_old_price,
                "new_price": new_price.text.strip(),
                "discount_details": discount_details.text.strip(),
                "label": '',
            })
    final_products.extend(products)


get_data()


for offer in final_products:
    data = requests.post(
        'https://shop-like-abed.herokuapp.com/deals', data=offer)
    print(data.json())
# random_number = random.randint(1, 200)
# with open(f'/tmp/data{random_number}.json', 'w',) as file:
#    json.dump(final_products, file, ensure_ascii=False)
