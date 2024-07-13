import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def get_about_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        about_link = None
        for link in soup.find_all('a', href=True):
            if 'about' in link['href'].lower():
                about_link = link['href']
                break

        if about_link is None:
            return "No about page found"

        if about_link.startswith('/'):
            from urllib.parse import urljoin
            about_link = urljoin(url, about_link)

        about_response = requests.get(about_link)
        about_response.raise_for_status()

        about_soup = BeautifulSoup(about_response.text, 'html.parser')

        
        for elem in about_soup.find_all(['header', 'footer']):
            elem.decompose()

        
        main_content = about_soup.find('main') or about_soup.find('div', {'role': 'main'})
        if main_content:
            return main_content.get_text(strip=True)
        else:
            return about_soup.get_text(strip=True)

    except requests.RequestException as e:
        return f"An error occurred: {e}"
file = open('mydata.xlsx','w')
file = csv.writer(file)
file.writerow(['website','data'])
df = pd.read_excel('Group 6&7-Websites.xlsx')
for column in df.columns:
    print(column)
    for url in df[column]:
        url= str(url)
        # if url==url.startswith('www') or url==url.startswith('http') :
        #     continue
        print(f"urlname:  {url}")
        if url.startswith('https://'):
            print(f"Processing URL: {url}")
            website_url = str(url)
            about_page_content = get_about_page_content(website_url)
            print(about_page_content)
            file.writerow([website_url,about_page_content])

        else:
            url="https://"+url
            print(f"Processing URL: {url}")
            website_url = str(url)
            about_page_content = get_about_page_content(website_url)
            print(about_page_content)
            file.writerow([website_url,about_page_content])


    