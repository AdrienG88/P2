import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/index.html'

response = requests.get(url)
soup = BeautifulSoup(response.text, features="html.parser")


def scrape_categories_url():
    if response.ok:
        cat_soup = soup.find('ul', class_='nav nav-list').find_all('a')
        i = 1
        cat_links = []
        while i < len(cat_soup):
            extracted_link = cat_soup[i].get('href')
            link = extracted_link.replace('catalogue/', 'https://books.toscrape.com/catalogue/')
            cat_links.append(link)
            i += 1

        with open('all_categories_urls.csv', 'w') as file:
            for elt in cat_links:
                file.write(elt)
                file.write(', ')


scrape_categories_url()
