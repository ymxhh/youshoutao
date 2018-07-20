# coding=utf-8
import requests
import re
import random
import time
import copy
import logging
import os
import platform


# 去除无效的链接
def remove_invalid_urls(urls):
    active_urls=[]
    for i in range(0, len(urls)):
        print(urls[i])
        # 先把如果指向的是当页的去除掉
        if urls[i] == "/":
            continue
        # 如果是JS的，先去掉
        elif urls[i] == "javascript:;":
            continue
        elif urls[i] == "javascript:history.go(-1)":
            continue
        # 如果是不明确的，先去除掉
        elif urls[i] == "/game/<%$value.spelling%>-<%$value.id%>-13-3":
            continue
        # 如果是不明确的，先去除掉
        elif urls[i] == "/taoid_<%$value.id%>.html":
            continue
        # 如果是不明确的，先去除掉
        elif re.search(r'<%\$value.nextUrl%>', urls[i]):
            continue
        # 如果是不明确的，先去除掉
        elif re.search(r'taoid_<%\$value\.id%>\.html', urls[i]):
            continue
        # 如果是不明确的，先去除掉
        elif urls[i] == "#":
            continue
        # 如果是web-app的域名，排除掉
        elif re.search(r'help-\d+-\d+\.html', urls[i]):
            continue
        # mqqwpa://im/chat?chat_type=crm&uin=800121938&version=1&src_type=web
        elif re.search(r'mqqwpa://im/chat\?chat_type=crm&uin=\d+&version=\d+&src_type=web', urls[i]):
            pass
        else:
            active_urls.append(urls[i])
    return active_urls


# 去重
def distinct(urls):
    print("移除非法链接后的:{}".format(urls))
    urls_new=[]
    for url in urls:
        if url not in urls_new:
            urls_new.append(url)
    print("去重后的URL:{}".format(urls))
    return urls_new


'''
@urls,需要做处理的URL列表
@amount，允许同类型存在的数量，比如如果为1，则表示此列表只允许同类型URL存在一个，一般用于当前页面的所有URL去重去同类处理，
如果为2，表示允许此列表里的URL同类型的存在2个，一般用于与已经访问过的页面做对比，在此为了扫描多个商品详情页和商品列表页。
@youxi_liebiao:游戏列表页的固定格式，将此类链接归纳到相似链接里
@youxi_search:通过首字母搜索，将此类链接归纳到相似链接里
@shangpin_liebiao:商品列表页，将此类链接归纳到相似链接里
@shangping_xiangqing:商品详情页的固定格式，将此类链接归纳到相似链接里
@edit_shangping:商品编辑页/上架页面的固定格式，将此类链接归纳到相似链接里
@buy_orders:买到的宝贝
@seller_orders:卖出的宝贝
@chongzhi_liebiao:充值列表
@tixian_liebiao：提现列表
@fabu:发布商品页
'''


def new_urls(urls, amount=1):
    # 先去重
    print("去重前的URL:{}".format(urls))
    if amount == 1:
        urls = distinct(urls)
    else:
        pass
    urls_new = []
    youxi_liebiao = []
    youxi_search = []
    shangping_liebiao = []
    shangping_xiangqing = []
    edit_shangping = []
    buy_orders = []
    seller_orders = []
    chongzhi_liebiao = []
    tixian_liebiao = []
    fabu = []
    chengpinghao_liebiao = []
    cailiao_liebiao = []
    zhuangbei_liebiao = []
    jinbi_liebiao = []
    zuanshi_liebiao = []
    shouchong_liebiao = []
    xuchong_liebiao = []
    pingguodaichong_liebiao = []
    anzuodaichong_liebiao = []
    for url in urls:
        if re.search(r'/game\?goodsid=\d+(&|&amp;)parentid=\d+', url):
            youxi_liebiao.append(url)
        elif re.search(r'/game/[a-zA-Z0-9_]+-\d+-\d+-\d+', url):
            shangping_liebiao.append(url)
        elif re.search(r'/games/list/index\?letter=\w{1}', url):
            youxi_search.append(url)
        elif re.search(r'/taoid_\d+.html', url):
            shangping_xiangqing.append(url)
        elif re.search(r'/user/my-posted-edit-trade-game-account/index?id=\d+', url):
            edit_shangping.append(url)
        elif re.search(r'/user/trade/info\?id=\d+',url):
            buy_orders.append(url)
        elif re.search(r'/user/seller/tradelogdesc\?tradelogid=\d+', url):
            seller_orders.append(url)
        elif re.search(r'/user/assets/info\?paytype=2&assetid=\d+',url):
            chongzhi_liebiao.append(url)
        elif re.search(r'/user/assets/withdraw-info\?assetid=\d+',url):
            tixian_liebiao.append(url)
        elif re.search(r'/user/selltrade/sellinfo\?gameid=\d+',url):
            fabu.append(url)
        # 非类似结构的URL先组成新的URLS列表
        else:
            urls_new.append(url)
    if amount==1:
        # 如果得到了商品列表，则随机选择一款游戏，扫描此游戏的所有类型商品
        if len(shangping_liebiao) > 0:
            # 得到游戏ID
            youxi_url = re.findall(r'(/game/[a-zA-Z0-9_]+-\d+)-\d+-\d+', random.choice(shangping_liebiao))
            # 成品号
            chengpinghao_liebiao.append(youxi_url[0] + "-20-1")
            urls_new.append(chengpinghao_liebiao[0])
            # 道具材料
            cailiao_liebiao.append(youxi_url[0] + "-14-15")
            urls_new.append(cailiao_liebiao[0])
            # 道具装备
            zhuangbei_liebiao.append(youxi_url[0] + "-14-16")
            urls_new.append(zhuangbei_liebiao[0])
            # 金币游戏币
            jinbi_liebiao.append(youxi_url[0] + "-5-17")
            urls_new.append(jinbi_liebiao[0])
            # 金币钻石
            zuanshi_liebiao.append(youxi_url[0] + "-5-19")
            urls_new.append(zuanshi_liebiao[0])
            # 首充号
            shouchong_liebiao.append(youxi_url[0] + "-13-3")
            urls_new.append(shouchong_liebiao[0])
            # 续充
            xuchong_liebiao.append(youxi_url[0] + "-13-9")
            urls_new.append(xuchong_liebiao[0])
            # 苹果代充
            pingguodaichong_liebiao.append(youxi_url[0] + "-10-11")
            urls_new.append(pingguodaichong_liebiao[0])
            # 安卓代充
            anzuodaichong_liebiao.append(youxi_url[0] + "-10-12")
            urls_new.append(anzuodaichong_liebiao[0])
        # 在其他的URL里所有类似结构的链接里只随机取一个，组成新的URL列表
        if len(youxi_liebiao) > 0:
            urls_new.append(random.choice(youxi_liebiao))
        if len(youxi_search) > 0:
            urls_new.append(random.choice(youxi_search))
        if len(chengpinghao_liebiao) > 0:
            urls_new.append(random.choice(chengpinghao_liebiao))
        if len(cailiao_liebiao) > 0:
            urls_new.append(random.choice(cailiao_liebiao))
        if len(zhuangbei_liebiao) > 0:
            urls_new.append(random.choice(zhuangbei_liebiao))
        if len(jinbi_liebiao) > 0:
            urls_new.append(random.choice(jinbi_liebiao))
        if len(zuanshi_liebiao) > 0:
            urls_new.append(random.choice(zuanshi_liebiao))
        if len(shouchong_liebiao) > 0:
            urls_new.append(random.choice(shouchong_liebiao))
        if len(xuchong_liebiao) > 0:
            urls_new.append(random.choice(xuchong_liebiao))
        if len(anzuodaichong_liebiao) > 0:
            urls_new.append(random.choice(anzuodaichong_liebiao))
        if len(pingguodaichong_liebiao) > 0:
            urls_new.append(random.choice(pingguodaichong_liebiao))
        if len(shangping_xiangqing) > 0:
            urls_new.append(random.choice(shangping_xiangqing))
        elif len(edit_shangping) > 0:
            urls_new.append(random.choice(edit_shangping))
        elif len(buy_orders) > 0:
            urls_new.append(random.choice(buy_orders))
        elif len(seller_orders) > 0:
            urls_new.append(random.choice(seller_orders))
        elif len(chongzhi_liebiao) > 0:
            urls_new.append(random.choice(chongzhi_liebiao))
        elif len(tixian_liebiao) > 0:
            urls_new.append(random.choice(tixian_liebiao))
        elif len(fabu) > 0:
            urls_new.append(random.choice(fabu))
        return urls_new
    elif amount > 1:
        if len(youxi_liebiao) > 1 or len(youxi_search) > 1 or len(shangping_liebiao) > amount*9 or len(shangping_xiangqing) > amount \
                or len(edit_shangping) > amount or len(buy_orders) > amount or len(seller_orders) > amount \
                or len(chongzhi_liebiao) > 1 or len(tixian_liebiao) > 1 or len(fabu) > amount:
            return False
        else:
            return True


#  通过登录获取用户信息
def get_session():
    try:
        response = requests.post(loginData['loginApi'],data=loginData['postData'], timeout=3)
    except requests.exceptions.Timeout:
        network_status = False
        if network_status is False:
            for i in range(1, 5):
                global j
                j = j+1
                if j < 5:
                    logger.info("连接超时，第{}次重新连接".format(j))
                    get_session()
                else:
                    quit()
    except Exception as e:
        print(e)
        raise Exception
    else:
        if response.status_code == 200:
            phpsessionid = re.findall(r'PHPSESSID=(\w+);', response.headers['Set-Cookie'])
            return phpsessionid[0]
        else:
            logger.info(u'访问用户信息失败,响应状态码：{}'.format(response.status_code))
            quit()


# 扫描
def scan(url):
    # 延时请求，避免被服务器拒绝
    time.sleep(random.randint(1, 3))
    sessionID = {"PHPSESSID": "{}".format(get_session())}
    try:
        # 带cookie可以访问需要登录才能访问的页面
        response = requests.get(url, cookies=sessionID, timeout=3)
    except requests.exceptions.Timeout:
        network_status = False
        if network_status is False:
            for i in range(1, 5):
                global j
                j = j + 1
                if j < 5:
                    logger.info("连接超时，第{}次重新连接,超时的URL:{}".format(j, url))
                    scan(url)
                else:
                    quit()
    except Exception as e:
        print(e)
        logger.error(e)
    else:
        print("要访问的页面:{}".format(url))
        visited.append(url)
        print('visited:{}'.format(visited))
        # 检查页面
        if response.status_code == 404 or response.status_code == 500:
            print("访问异常的页面：{}".format(url))
        else:
            if re.search('错误信息',response.text):
                print("访问异常的页面：{}\n返回的内容如下：{}".format(url, response.text))
                except_url.append(url)
            else:
                # 将获取的URL坐下处理，只取有效的URL，避免多次访问同样的URL,只会返回（）里的内容
                # a:<a\s[^>]*\s?href=["]([^"]*)["]
                # div:
                matchs1 = re.findall(r'<a\s[^>]*\s?href=["]([^"]*)["]', response.text)
                matchs2 = re.findall(r'<div\s[^>]*\s?data-href=["]([^"]*)["]', response.text)
                print(matchs2)
                matchs=matchs1+matchs2
                print("处理前的URL：{}".format(matchs))
                matchs = remove_invalid_urls(matchs)
                # 对URL做处理，让相同结构的只取一个
                urls=new_urls(matchs)
                print("处理后的URL如下:{}".format(urls))
                if len(urls) > 0:
                    for url in urls:
                        # 如果包含了主域名，则是一个完整的域名，后面只需直接请求，列如广告位
                        if url.find(base) >= 0:
                            url=url
                        # 如果包含了非淘手游主域名，直接退出当前循环，直接检测下一个URL，注意正则要排除掉详情页，列如/taoid_5967340.html
                        elif re.search(r'^[^/][a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+', url):
                            continue
                        else:
                            # 剩下的只有具体地址的链接，需要与baseURL结合，用于后面访问
                            url = base + url
                        if url == baseUrl:
                            continue
                        # 之前已经访问过的URL，则退出当前循环,不再扫描
                        elif url in visited:
                            continue
                        # 对商品列表、商品详情、编辑/上架商品的链接做特殊处理，避免访问太多不同游戏的商品列表和商品详情
                        # 方式：和已经访问的页面做格式判断，如果有类似的，表示已经访问过，退出当前循环
                        else:
                            visited_bak = copy.deepcopy(visited)
                            visited_bak.append(url)
                            # 这里允许最多访问两次同类型的商品，用备份的去做对比，避免影响visited本身
                            amount = 2
                            if new_urls(visited_bak, amount) is False:
                                continue
                            else:
                                scan(url)
                else:
                    pass


baseUrl = 'http://cdt0-microh5.taoshouyou.com/index'
base = 'http://cdt0-microh5.taoshouyou.com'
loginData = {'loginApi': 'http://cdt0-passport.taoshouyou.com/api/user/login',
             'postData': {'userName': 'grace2', 'password': '123456'}
             }
# 访问异常的页面
except_url = []
# 访问超时的页面
timeout_url = []
# 访问过的页面，用于后面判断，如果是已经访问过的页面，不再访问
visited = []
j = 0
if __name__ == '__main__':
    print(baseUrl)
    if baseUrl in visited:
        pass
    else:
        print('start')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        if 'Windows' in platform.system():
            log_path = os.path.dirname(os.path.abspath(__file__))+'\\'
        else:
            log_path = os.path.dirname(os.path.abspath(__file__))+'/'
        log_file = log_path+'scan_result.log'
        print('create log file')
        fh = logging.FileHandler(log_file, mode='w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s] %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        print('start scan')
        scan(baseUrl)
        print('end scan')
        visited_urls = ''
        for i in range(0, len(visited)):
            visited_urls = visited_urls+'\n\r'+visited[i]
        logger.info("已正常访问的页面如下:{}".format(visited_urls))
        logger.info("访问异常的页面：{}".format(except_url))
        print('end')
