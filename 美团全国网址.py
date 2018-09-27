import threading
import time
from urllib import request
from bs4 import BeautifulSoup
from multiprocessing import Pool

url = "https://www.meituan.com/changecity/"
headers = {
    'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'Accept-Encoding':' gzip, deflate',
'Accept-Language':' zh-CN,zh;q=0.9',
'Connection':' keep-alive',
'Cookie':' _lxsdk_cuid=16509a8a7dbc8-0ffaefc2fbed5b-2711639-144000-16509a8a7ddc8; __mta=46078747.1533465372655.1533601994261.1533602061951.5; iuuid=04CA67C6A4DB81A68AC3901617C50E8C0CC55B8C885891CDB87E73198AC1899C; cityname=%E9%82%B9%E5%B9%B3; _lxsdk=04CA67C6A4DB81A68AC3901617C50E8C0CC55B8C885891CDB87E73198AC1899C; ci=1; rvct=1%2C238%2C508%2C197%2C88; uuid=34b3e0f7b4634b4680bb.1537952958.1.0.0; client-id=38190958-dce4-463f-843f-267d2e97160b; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; lat=39.997991; lng=116.488551; _lxsdk_s=166157c8b62-7d3-ea7-1e1%7C%7C51',
'Host':' www.meituan.com',
# 'Referer': 'http://bj.meituan.com/meishi/pn1/',
'Upgrade-Insecure-Requests':' 1',
'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Mobile Safari/537.36'}

def country(url):
    req = request.Request(url,headers=headers)
    resp = request.urlopen(req)
    aaa = resp.read().decode("utf-8")
    soup = BeautifulSoup(aaa,'lxml')
    city_area = soup.select(".city-area > .cities > a")
    c_list = []
    for i in city_area:
        h = i.attrs['href']
        c_url = "http:" + h + "/meishi/"
        # print(c_url)
        c_list.append(c_url)
    return c_list

class MyThread(threading.Thread):
    """
        属性:
        target: 传入外部函数, 用户线程调用
        args: 函数参数
        """

    def __init__(self, target,args,krgs):
        super(MyThread, self).__init__()  # 调用父类的构造函数
        self.target = target
        self.args = args
        self.krgs= krgs

    def run(self):
        self.target(self.args,self.krgs)

def get_url(a,b):
    u_list = country(url)
    for i in u_list[a:b]:
        print(i)
        print("当前的线程是：" + threading.current_thread().name)
        time.sleep(1)

if __name__ == "__main__":

    th1 = MyThread(get_url,0,100)
    th2 = MyThread(get_url, 100, 200)
    th3 = MyThread(get_url, 200, 300)
    th1.start()
    th2.start()
    th3.start()

    th1.join()
    th2.join()
    th3.join()
    print("game over")