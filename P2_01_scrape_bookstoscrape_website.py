import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import shutil

url_main_page = 'https://books.toscrape.com/index.html'


def scrape_categories_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")

    if response.ok:
        cat_soup = soup.find('ul', class_='nav nav-list').find_all('a')
        cat_urls = []
        for i in range(1, len(cat_soup), 1):
            extracted_link = cat_soup[i].get('href')
            link = extracted_link.replace('catalogue/', 'https://books.toscrape.com/catalogue/')
            cat_urls.append(link)

    return cat_urls


def get_next_page_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')
    cat_all_urls = []
    if response.ok:
        cat_all_urls.append(url)
        next_page = soup.find('li', class_='next')
        if next_page:
            next_page_url = next_page.a.get('href')
            url_to_change = url.split('/')
            url_to_change[-1] = next_page_url
            url_new = '/'.join(url_to_change)
            cat_all_urls.append(get_next_page_urls(url_new))

    return cat_all_urls


f_lst = []
def flatten_list(lst):
    tmp_lst = []
    for elt in lst:
        if type(elt) == list:
            tmp_lst.append(elt)
            f_lst.append(tmp_lst[0])
            tmp_lst.pop()
            flatten_list(elt)
        else:
            tmp_lst.append(elt)
            f_lst.append(tmp_lst[0])

    final_list = list(set(f_lst))
    return final_list


def scrape_book_urls(url_list):
    book_urls = []
    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features='html.parser')
        if response.ok:
            url_list_raw = soup.find('ol', class_='row').find_all('a')

            for j in range(0, len(url_list_raw), 2):
                extracted_url = url_list_raw[j].get('href')
                url_in = extracted_url.replace('../../../', 'https://books.toscrape.com/catalogue/')
                book_urls.append(url_in)

    return book_urls


def scrape_book_info(url_list):
    info_list = []
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

    return info_list


def create_book_info_file(info_list):
    my_frame = pd.DataFrame(info_list)
    filename = info_list[0]['category'].replace(' ', '') + '.csv'
    my_frame.to_csv(filename, index=False)


def create_book_covers_dir(info_list):
    path = info_list[0]['category'].replace(' ', '') + '_book_covers'
    os.mkdir(path)


def dl_book_covers(info_list):
    for entry in info_list:
        r = requests.get(entry['image_url'], stream=True)
        r.raw.decode_content = True
        filename = info_list[0]['category'].replace(' ', '') + '_book_covers' + '/' + (entry['image_url'].split('/'))[-1]
        with open(filename, 'wb') as file:
            shutil.copyfileobj(r.raw, file)


def one_loop_to_run_them_all(current_scraped_page):

    all_pages_for_cat = get_next_page_urls(current_scraped_page)
    print('all_pages_for_cat: ', all_pages_for_cat)

    flat_all_pages_for_cat = flatten_list(all_pages_for_cat)
    print('flat_all_pages_for_cat: ', flat_all_pages_for_cat)

    cat_book_urls = scrape_book_urls(flat_all_pages_for_cat)
    print('cat_book_urls: ', cat_book_urls)
'''
    book_data_list = scrape_book_info(cat_book_urls)

    create_book_info_file(book_data_list)
    create_book_covers_dir(book_data_list)
    dl_book_covers(book_data_list)
'''

def one_script_to_run_them_all(url):
    cat_links = scrape_categories_urls(url)

    for link in cat_links:
        one_loop_to_run_them_all(link)

    # python P2_01_scrape_bookstoscrape_website.py


one_script_to_run_them_all(url_main_page)
