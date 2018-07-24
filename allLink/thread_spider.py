# coding: utf-8
'''
Created on 2018年7月24日

@author: 27419
'''
from queue import Queue 
from threading import Thread, Lock
import urllib.parse
import socket
import re
import time

seen_urls = set(['/'])  # 记录已经解析到的url地址
lock = Lock()   # 线程同时操作一个全局变量时会产生线程竞争所以需要锁

'''
继承线程类
'''
class Fetcher(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks  # tasks任务队列
        # 加这一步后主程序中断退出后子线程也会跟着中断退出
        self.daemon = True

        self.start()

    # 线程运行的函数
    def run(self):
        while True:
            url = self.tasks.get()  # 从队列得到一个item，队列为空则阻塞
            print(url)
            sock = socket.socket()
            sock.connect(('localhost', 3000))   # 链接到address处的套接字
            get = 'GET {} HTTP/1.0\r\nHost: localhost\r\n\r\n'.format(url)
            sock.send(get.encode('ascii'))  # sock.send(string[,flag])将string中的数据发送到链接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小
            response = b''
            chunk = sock.recv(4096) # send.recv(bufsize[,flag])接受套接字的数据。数据以字符串形式返回，bufsize指定最多可接收的数量。flag提供有关消息的其他信息，通常可以忽略
            while chunk:
                response += chunk
                chunk = sock.recv(4096)
            
            # 解析页面上所有链接
            links = self.parse_links(url, response)

            lock.acquire()  # 获得锁
            # ***操作全局变量seen_urls***
            # 得到新链接加入任务队列与seen_urls中
            for link in links.difference(seen_urls):
                self.tasks.put(link)    # 往队列里添加一个item，队列满了则阻塞
            seen_urls.update(links)
            # ***操作全局变量***   
            lock.release()  # 释放锁
            
            # 通知任务队列这个线程的任务完成了
            self.tasks.task_done()  # 线程告知任务完成使用task_done

    def parse_links(self, fetched_url, response):
        if not response:
            print('error: {}'.format(fetched_url))
            return set()
        if not self._is_html(response):
            return set()
        # 通过href属性找到所有链接
        urls = set(re.findall(r'''(?i)href=["']?([^\s"'<>]+)''',
                              self.body(response)))

        links = set()
        for url in urls:
            # 可能找到的url是相对路径，这时候就需要join一下，绝对路径的话就还是会返回url
            normalized = urllib.parse.urljoin(fetched_url, url)
            # url的信息会被分段存在parts里
            parts = urllib.parse.urlparse(normalized)
            if parts.scheme not in ('', 'http', 'https'):
                continue
            host, port = urllib.parse.splitport(parts.netloc)
            if host and host.lower() not in ('localhost'):
                continue
            # 有的页面会通过地址里的#frag后缀在页面内跳转，这里去掉frag的部分
            defragmented, frag = urllib.parse.urldefrag(parts.path)
            links.add(defragmented)

        return links

    # 得到报文的html正文
    def body(self, response):
        body = response.split(b'\r\n\r\n', 1)[1]
        return body.decode('utf-8')

    def _is_html(self, response):
        head, body = response.split(b'\r\n\r\n', 1)
        headers = dict(h.split(': ') for h in head.decode().split('\r\n')[1:])
        return headers.get('Content-Type', '').startswith('text/html')

'''
线程池类
'''
class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue()    # 创建一个队列，Queue(maxsize=0)，maxsize为队列大小，为0默认队列大小可无穷大
        for _ in range(num_threads):
            Fetcher(self.tasks)

    def add_task(self, url):
        self.tasks.put(url)     # 往队列添加一个item，队列满了则阻塞

    def wait_completion(self):
        self.tasks.join()       # 队列不为空，或者为空但是

if __name__ == '__main__':
    start = time.time()
    pool = ThreadPool(4)
    pool.add_task("/")
    pool.wait_completion()
    print('{} URLs fetched in {:.1f} seconds'.format(len(seen_urls),time.time() - start))
    
