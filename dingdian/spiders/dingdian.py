import scrapy
from scrapy.http import Request
import re
from bs4 import BeautifulSoup
from dingdian.items import DingdianItem, DcontentItem
from dingdian.mysqlpipelines.sql import Sql


class Myspider(scrapy.Spider):

    name = 'dingdian'
    allowed_domains = ['23us.com']
    bash_url = 'http://www.23us.com/class/'
    bashurl = '.html'

    def start_requests(self):
        for i in range(1, 11):
            url = self.bash_url + str(i) + '_1' + self.bashurl
            yield Request(url, self.parse)

    def parse(self, response):
        response_soup = BeautifulSoup(response.text, 'lxml')
        max_num = response_soup.find(
            'div', class_='pagelink').find_all('a')[-1].get_text()
        bashurl = str(response.url)[:-7]

        for num in range(1, int(max_num) + 1):
            url = bashurl + '_' + str(num) + self.bashurl
            yield Request(url, callback=self.get_name)

    # 获取小说名
    def get_name(self, response):
        tbs = BeautifulSoup(response.text, 'lxml').find_all(
            'tr', bgcolor='#FFFFFF')
        for td in tbs:
            novelname = td.find('a').get_text()
            novelurl = td.find('a')['href']
            # meta向下传递值
            yield Request(novelurl, callback=self.get_chapterurl, meta={'name': novelname, 'url': novelurl})

    # 获取小说地址url
    def get_chapterurl(self, response):
        # 实例化
        item = DingdianItem()
        # \xao是为了替换空字符&nbsp
        item['name'] = str(response.meta['name']).replace('\xa0', '')
        item['novelurl'] = response.meta['url']
        all_start = BeautifulSoup(response.text, 'lxml').find('table', id='at')
        category = all_start.find('a').get_text()
        author = all_start.find_all('td')[1].get_text().replace('\xa0', '')
        chapter_list_url = BeautifulSoup(response.text,'lxml').find('a', class_='read')['href']
        # http://www.23us.com/book/ = 25 得到尾部数字
        length = len(item['novelurl']) - 25
        name_id = item['novelurl'][-length:]
        item['category'] = category
        item['author'] = author
        item['name_id'] = name_id
        yield item
        yield Request(chapter_list_url, callback=self.get_chapter, 
                      meta={'name_id': name_id, 'chapter_list_url': chapter_list_url})

    # 获取小说章节
    def get_chapter(self, response):
        urls = BeautifulSoup(response.text, 'lxml').find(
            'table', id='at').find_all('a')
        # 因为Scrapy是异步运行,采集的章节顺序混乱,需要排序,按照这个排序就能得到正确的章节顺序
        num = 0

        for url in urls:
            num = num + 1
            chapterurl = response.meta['chapter_list_url'] + url['href']
            chaptername = url.get_text()
            yield Request(chapterurl, callback=self.get_chaptercontent,
                          meta={'num': num, 'name_id': response.meta['name_id'], 'chapterurl': chapterurl, 'chaptername': chaptername})

    # 获取小说章节内容
    def get_chaptercontent(self, response):
        # 实例化
        item = DcontentItem()
        item['num'] = response.meta['num']
        item['id_name'] = response.meta['name_id']
        item['chaptername'] = response.meta['chaptername'].replace('\xa0', '')
        item['chapterurl'] = response.meta['chapterurl']
        content = BeautifulSoup(response.text, 'lxml').find(
            'dd', id='contents').get_text().replace('\xa0', '')
        item['chaptercontent'] = content
        return item
