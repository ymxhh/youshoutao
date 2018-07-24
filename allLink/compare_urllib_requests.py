# coding: utf-8
'''
Created on 2018年7月24日

@author: 27419
'''

import requests
import urllib.request

# requests
req1 = requests.get('http://cdt0-web.taoshouyou.com/games/search?wd=%E7%AC%AC%E4%BA%94%E4%BA%BA%E6%A0%BC',
                   headers={
                       'Connection': 'Keep-Alive',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                    })
f = open(r'../output/req.html', 'wb')
f.write(req1.text.encode())
f.close()

# urllib.requests
req2 = urllib.request.Request('http://cdt0-web.taoshouyou.com/games/search?wd=%E7%AC%AC%E4%BA%94%E4%BA%BA%E6%A0%BC',
                   headers={
                       'Connection': 'Keep-Alive',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                    })
rlb = urllib.request.urlopen(req2)
f = open(r'../output/rlb.html', 'wb')
f.write(rlb.read())
f.close()