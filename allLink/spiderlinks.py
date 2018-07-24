# coding: utf-8
'''
Created on 2018年7月17日

@author: 27419
'''

import requests
import re
import time

'''
获取url中的链接
'''
def spiderpage(url):

    try:
#         kv = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'}
#         kv = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'}
#         r = requests.get(url, headers=kv)
        r = requests.get(url)
    except:
        print("url cannot link")
        
    r.encoding = r.apparent_encoding    # 使用apparent_encoding可以获得真实编码
    
    pagetext = r.text
    # write(pagetext, r'./pagetext-goods.txt', 'w')
    
    # 正则表达式表示要爬取的是<a href="和"中的内容,"或'都可以,即当前页面下所有的链接url,返回列表
    # (?<=...) 之前的字符串内容需要匹配表达式才能匹配成功。不消耗字符串内容。
    pagelinks = re.findall(r'(?<=<a href=\").*?(?=\")|(?<=href=\').*?(?=\')', pagetext)
    
    # for i in range(len(pagelinks)):
    #     write(pagelinks[i]+'\n', r'./pagelinks-goods.txt', 'a')
    
    return pagelinks

'''
过滤urls，得到目标url
'''
def filter_url(pagelinks, base_domain):
    target_url = []
    for link in pagelinks:
#         print('待验证的url：', link)
#         if re.match(r'(http://www.taoshouyou.com).*?|(https://www.taoshouyou.com).*?|(/).+?', link):
#         if re.match(r'(http://www.taoshouyou.com).*?|(https://www.taoshouyou.com).*?|(https://).*?(.taoshouyou.com)|(http://).*?(.taoshouyou.com)', link):
        if re.match(r'(https://).*?(.taoshouyou.com)|(http://).*?(.taoshouyou.com)', link):
            target_url.append(link)
#             print(r'    验证通过：\n', link)
        elif re.match(r'(/).+?', link):
#             link = 'http://www.taoshouyou.com' + link
#             link = 'https://m.taoshouyou.com' + link
            link = base_domain + link
#             print(r'    验证通过：\n', link)
            target_url.append(link)
#     print(r'**以下为验证通过的link集合**')
#     for link in target_url:
#         print(link)
    return target_url

'''
link队列
'''
class linkQuence:
    def __init__(self):
        # 已访问的url集合
        self.visited = []
        # 待访问的url集合
        self.unvisited = []

    # 获取访问过的url队列
    def get_visited(self):
        return self.visited

    # 获取未访问的url队列
    def get_unvisited(self):
        return self.unvisited

    # 添加url到访问过得队列中（队尾）
    def add_visited(self, url):
        return self.visited.append(url)

    # 移除访问过得url
    def remove_visited_url(self, url):
        return self.visited.remove(url) # 移除某个值的第一个匹配项

    # 从未访问队列中取一个url（队尾）
    def pop_unvisited(self):
        try:
            return self.unvisited.pop() # pop([index=-1])移除一个元素并返回该元素值（默认最后一个）
        except:
            return None

    # 添加url到未访问的队列中（队首）
    def add_unvisited(self, url):
        if url != "" and url not in self.visited and url not in self.unvisited:
            return self.unvisited.insert(0, url)    # insert(index, obj)将对象插入到指定index位置

    # 获得已访问的url数目
    def get_visited_count(self):
        return len(self.visited)

    # 获得未访问的url数目
    def get_unvisted_count(self):
        return len(self.unvisited)

    # 判断未访问的url队列是否为空
    def unvisited_isempty(self):
        return len(self.unvisited) == 0
    

class Spider():
    def __init__(self, url, base_domain):
        self.linkQuence = linkQuence()  # 将队列引入本类
        self.linkQuence.add_unvisited(url)  # 传入待爬取的url,即入口
        self.base_domain = base_domain

    def crawler(self, urlcount):
        # 子页面过多,为测试方便加入循环控制子页面数量
        x = 1
        while x <= urlcount:
            # 若子页面不是很多,可以直接使用队列中的未访问列表非空作为循环条件
            # while not self.linkQuence.unvisited_isempty():
            if x > 1:
                print(f"第{x-1}个url,开始爬")
            visitedurl = self.linkQuence.pop_unvisited()  # 从未访问列表中pop出一个url
            print(visitedurl)
            if visitedurl is None or visitedurl == '':  # 初始状态
                continue
            initial_links = spiderpage(visitedurl)  # 爬出该url页面中所有的链接
            right_links = filter_url(initial_links, base_domain) # 筛选出合格的链接
            self.linkQuence.add_visited(visitedurl)  # 将该url放到访问过的url队列中
            for link in right_links:  # 将筛选出的链接放到未访问队列中
                self.linkQuence.add_unvisited(link)
#             for i in range(len(right_links)):
#                 self.linkQuence.add_visited(right_links[i])
            x += 1
        print(f"终于爬完了,一共是{x-2}个url")    # ？？？
        return self.linkQuence.visited
    
'''
有点问题（when mode='a'）
'''
def write(content, path, mode='w'):
    file = open(path, mode, encoding='utf-8')
    file.write(content)
    file.close()
    

    

if __name__ == '__main__':
#     spiderpage(r'https://www.taoshouyou.com')
#     pagelinks = spiderpage(r'https://www.taoshouyou.com/game/wangzherongyao-2256-20-1')
#     pagelinks = spiderpage(r'https://www.taoshouyou.com//taoid_8485076.html')
#     pagelinks = spiderpage(r'http://www.taoshouyou.com/user/buy-trade-game-account?tradeid=10748691&buynum=1')
    
#     url = r'http://www.cdt0-microh5.taoshouyou.com'
#     url = r'http://microh5.taoshouyou.com/index'

    url = r'https://m.taoshouyou.com'
#     base_domain = r'https://m.taoshouyou.com'
    base_domain = url
    
#     pagelinks = spiderpage(url, base_domain)
#     filter_url(pagelinks)

    t = time.time()
    start_time = time.strftime('%Y-%m-%d %H:%M:%S')
    spider = Spider(url, base_domain)
    #传入要爬取的子链接数量
    url_list = spider.crawler(10)
    end_time = time.strftime('%Y-%m-%d %H:%M:%S')
    file = open(r'../output/urllist_'+str(t)+r'.txt', 'a', encoding='utf-8')
    file.write(start_time+'\n')
    file.write(end_time+'\n')
 
    for link in url_list:
        file.write(link+'\n')

    file.close()
