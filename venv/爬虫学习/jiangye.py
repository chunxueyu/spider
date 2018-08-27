from urllib import request
from bs4 import BeautifulSoup
import time
import random

url = "http://www.booktxt.com/book/0/754/"
agentList = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
]

def getHtml(url):
    agentStr = random.choice(agentList)      #随机一个代理
    mheader = {"Referer": "http://www.booktxt.com/0_754/",
               "User-Agent": agentStr}
    req = request.Request(url,headers=mheader)
    page = request.urlopen(req)
    html = page.read().decode("gb2312",errors="ignore")      #error有错误忽视
    return html
#print(getHtml(src))

def getallUrl(html):
    soup = BeautifulSoup(html,'html.parser')
    all = soup.find('div',id = 'list').find_all('a')    #找到所有a标签
    Dict = {}
    print(all)
    for li in all:
        # print("********")
        # print(li)
        s = li.attrs['href']    #获得拼接的链接
        # print(s)
        b=li.get_text()         #获得文本
        Dict.setdefault(s,b)    #把网址添加到字典
    #print(Dict)
    return Dict

def enterhtml(Dict):
    for k,v in Dict.items():
        newurl = 'http://www.booktxt.com' + k
        #print(newurl)
        html = getHtml(newurl)
        soup = BeautifulSoup(html, 'html.parser')
        alltext = soup.find('div', id='content')           #找到小说文本
        b = alltext.get_text().replace(u'\xa0',u' ')        #把空格"\xa0"替换成空格
        #print(b)
        file = open("d:\\将夜.txt", "a")
        file.write(v)          #写入标题
        file.write("\r\n")     #换行写入
        file.write(b)          #写入文本
        file.write("\r\n")
        time.sleep(0.5)
        print(v)
    file.close()


enterhtml(getallUrl(getHtml(url)))
