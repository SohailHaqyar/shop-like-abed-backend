import requests
from bs4 import BeautifulSoup


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
    final_products.extend(products)
    if len(products) != 0:
        get_data(pageNumber+1)


get_data(1)
print(len(final_products))
print(final_products)
