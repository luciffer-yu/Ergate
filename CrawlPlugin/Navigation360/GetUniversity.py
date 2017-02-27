#-*- coding: utf-8 -*-
from Utility import URLRequset
from bs4 import BeautifulSoup
import re

class UniversityInfo(URLRequset.UrlOpen):
    def __init__(self, timeout, retry, url='http://edu.360.cn/daxue'):
        URLRequset.UrlOpen.__init__(self, timeout, retry)
        self.url = url
        self.province = {}

    def start_crawling(self):
        self.__CrawlingMainPage__(self.GetPage(self.url))
        return self.province

    def __CrawlingMainPage__(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        node = soup.find_all('h2', class_='tit', string = '全国大学名录', limit=1)
        tables = node[0].find_all_next('ul', class_='ui-tlist-h ui-tlist-1')
        for child in tables[0]:
            pro_str = child.string.strip()
            if pro_str:
                pattern = re.compile('.*(?=\()')
                mt = pattern.match(pro_str)
                #group(0) is province info,and it will be matched the info of university dicts
                self.province[mt.group(0)] = self.__Crawling_university_sub_page__(self.GetPage(child.next_element.get('href')))

    def __Crawling_university_sub_page__(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        tables = soup.find_all('ul', class_='ui-tlist-h ui-tlist-1')
        univers = {}
        for table in tables:
            for child in table.children:
                try:
                    if child.string.strip():
                        univers[child.string.strip()] = child.next_element.get('href')
                except:
                    pass
        return univers



