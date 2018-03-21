# -*- coding:utf-8 -*-
import time
import os
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Pool

__author__ = 'Hippo'


class Comic(object):

    def scroll(self, x, y):
        # 用于滚动页面加载完整图片URL
        return "window.scrollTo(0,(document.body.scrollHeight/{0})*{1}*20);".format(x, y)

    def get_picutre_url(self, url):
        # 获取章节图片URL并下载至本地
        comics = {}
        comic_url = []
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        driver.get(url)
        time.sleep(2)
        x = 10
        for y in range(0, x+1):
            s = self.scroll(x, y)
            print(s)
            driver.execute_script(s)
            time.sleep(random.randint(1, 5))
        content = driver.page_source
        # print(content)
        soup = BeautifulSoup(content, "lxml")
        comic_list = soup.find_all('li', attrs={'style': True})
        comic_title = soup.find('span', attrs={'class': 'title-comicHeading'}).text.strip()
        for i in comic_list:
            # print(i)
            try:
                image_url = i.find('img')['src']
                comic_url.append(image_url)
            except Exception as e:
                print(e)
        comics['title'] = comic_title
        comics['url'] = comic_url
        title = comics['title']
        urls = comics['url']
        driver.close()
        directory = 'D:\\manhua\\中国惊奇先生\\' + title
        if not os.path.exists(directory):
            os.makedirs(directory)
            print('Downloading ' + directory + '.....Please Waiting')
            for download_link in urls:
                time.sleep(random.randint(1, 5))
                fname = directory + '\\' + str(urls.index(download_link) + 1) + '.png'
                if os.path.exists(fname):
                    # pass
                    print('File ' + fname + ' is already exists,SKIP......')
                else:
                    #     print ('Folder is already exists,Downloading '+directory+'.....Please Waiting')
                    r = requests.get(download_link)
                    with open(fname, "wb") as code:
                        code.write(r.content)
                    print(fname + ' Download Compelte')
            return  # Pool的map函数需要返回任意值才能结束进程
        else:
            print('File ' + directory + ' is already exists,SKIP......')
            return

    def get_page_url(self, url):
        # 获取所有章节URL
        page_url_list = []
        if url is None:
            return None
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.content, "lxml")
            item_list = soup.find_all("span", attrs={'class': 'works-chapter-item'})
            for i in item_list:
                try:
                    item=i.find('a')['href']
                    page_url = 'http://ac.qq.com'+item
                    page_url_list.append(page_url)
                except Exception as e:
                    print(e)
        return page_url_list


if __name__ == '__main__':
    comic = Comic()
    item_url=comic.get_page_url('http://ac.qq.com/Comic/comicInfo/id/511915')
    pool = Pool(processes=2)
    pool.map(comic.get_picutre_url, item_url)
    pool.close()
    pool.join()
