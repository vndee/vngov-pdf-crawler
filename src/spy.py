import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from urllib import request


class Spy:

    def __init__(self, domain, out_dir):
        self.domain = domain
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(firefox_options=options)

    def crawl(self, dm=None):
        if dm is None:
            dm = self.domain

        self.driver.get(dm)
        content = self.driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        list_documents = soup.find_all('a', class_='doc_list_link', href=True)
        next_page_action = soup.find_all('a', class_='pageAction', href=True)[0]

        for doc in list_documents:
            self.download_pdf(doc['href'])

        self.crawl(next_page_action['href'])

    def download_pdf(self, link):
        self.driver.get(link)
        content = self.driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        pdf_link = soup.find_all('a', class_='doc_detail_file_link', href=True)
        for li in pdf_link:
            print('Downloading', li['href'])
            request.urlretrieve(li['href'], os.path.join(self.out_dir, li['href'].split('/')[-1]))

    def __del__(self):
        self.driver.quit()
        print('DONE')
