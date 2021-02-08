import requests
from bs4 import BeautifulSoup
import csv

# url_input = input("Veuillez entrer l'URL de la première page de la catégorie: ")
url_input = 'https://books.toscrape.com/catalogue/category/books/young-adult_21/page-1.html'
cat_book_urls = []
book_data_list = []


def scrape_book_urls(url, url_list):
    cat_book_urls = url_list
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")

    if response.ok:
        page_book_urls_raw = soup.find('ol', class_='row').find_all('a')

        j = 0
        # prélève les url de livres dans une page de cat
        while j < len(page_book_urls_raw):
            extracted_url = page_book_urls_raw[j].get('href')
            url_in = extracted_url.replace('../../../', 'https://books.toscrape.com/catalogue/')
            cat_book_urls.append(url_in)
            j += 2

        next_page = soup.find('li', class_='next')
        if next_page:
            next_page_url = next_page.a.get('href')
            url_to_change = url.split('/')
            url_to_change[-1] = next_page_url
            url_new = '/'.join(url_to_change)
            cat_book_urls += scrape_book_urls(url_new, cat_book_urls)
        # else:
        #    print('cat_book_urls', cat_book_urls)

    return cat_book_urls


scrape_book_urls(url_input, [])

# PROBLEME: Appeler la valeur de cat_book_urls retournée par scrape_book_urls

cat_book_urls = ['https://books.toscrape.com/catalogue/girl-online-on-tour-girl-online-2_101/index.html',
                 'https://books.toscrape.com/catalogue/the-haters_67/index.html',
                 'https://books.toscrape.com/catalogue/the-art-of-not-breathing_58/index.html']


def scrape_book_info(url_list, info_list):

    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="html.parser")

        if response.ok:
            product_page_url = url
            upc = soup.find('th', string='UPC').next_sibling
            title = soup.find('div', class_='col-sm-6 product_main').find('h1')
            price_including_tax = soup.find('th', string='Price (incl. tax)').next_sibling
            price_excluding_tax = soup.find('th', string='Price (excl. tax)').next_sibling
            number_available = soup.find('p', class_='instock availability')
            product_description = soup.find('h2', string='Product Information').find_parent('div').find_previous('p')
            category = soup.find('li', class_='active').find_previous('li')
            review_rating = soup.find('i', class_='icon-star').find_parent('p').get('class')
            image_url = soup.find('div', class_='item active').find('img').get('src')

            info_dict = {'product_page_url': product_page_url,
                         'universal_product_code (upc)': upc.text,
                         'title': title.text,
                         'price_including_tax': price_including_tax.text.replace('Â', ''),
                         'price_excluding_tax': price_excluding_tax.text.replace('Â', ''),
                         'number_available': number_available.text.strip(),
                         'product_description': product_description.text,
                         'category': category.text.strip(),
                         'review_rating': (review_rating[1].lower() + ' out of five'),
                         'image_url': image_url.replace('../../', 'https://books.toscrape.com/')
                         }

            info_list.append(info_dict)

            filename = info_dict['category'].replace(' ', '') + '.csv'
            with open(filename, 'w') as file:
                #for index in info_dict:
                #    file.write(index)
                fieldnames = ('product_page_url', 'universal_product_code (upc)', 'title',
                              'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description',
                              'category', 'review_rating', 'image_url')
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for entry in info_list:
                    writer.writerow(entry)
# 2 problems : only first entry is taken and encoding problem (maybe linked)

scrape_book_info(cat_book_urls, book_data_list)
