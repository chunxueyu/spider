import json

import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"}

# 登录的时候有2个token值随着每次访问登录页的不同而改变，验证码也是随着每次访问而不同，我们要获取这些值需要先访问一次登录页，然后从登录页中提取，再进行登录

# 登录的url
login_url = "https://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx"

# 创建session对象
s = requests.session()
login_page = s.get(url=login_url)
res = login_page.text

# 提取token值和验证码
soup = BeautifulSoup(res,'lxml')
# 提取token值
a = soup.select("#__VIEWSTATE")[0].attrs.get("value")
b = soup.select("#__VIEWSTATEGENERATOR")[0].attrs.get("value")
c = soup.select("#imgCode")[0].attrs["src"]
img_url = "https://so.gushiwen.org"+c
# print(a,b)
# print(img)
# 下载验证码
img = s.get(img_url)
# print(img.content)
with open("./yanzhengma.png",'wb') as fp:
    fp.write(img.content)

# 输入验证码
code_num = input("请输入验证码：")
# 构建请求体
data = {
    "__VIEWSTATE":a,
    "__VIEWSTATEGENERATOR":b,
    "form":"http://so.gushiwen.org/user/collect.aspx",
    "email": "fanjianbo666@163.com",
    "pwd": "123456",
    "code": code_num,
    "denglu": "登录"
}
res = s.post(url=login_url,headers=headers,data=data)
# print(res.text)

# 抓取主页得内容：收藏的所有的名句，古诗，古籍，以及作者，存入json文件
# 定义一个列表，存储四个url的type参数
page_url = "https://so.gushiwen.org/user/collect.aspx?"
types = ['s','m','a','d']
# 创建一个列表，用于解析
items = []
for type in types:
    # 定制参数
    data = {
        'type':type,
        'id':'201868',
        'sort':'t',
        "x":""
    }
    page = s.get(url=page_url,headers=headers,params=data)
    soup = BeautifulSoup(page.text,"lxml")
    # 解析页面
    if type == "s":
        # 诗文 取作者，内容，标题
        titles = soup.select(".cont p b")
        authors = soup.select(".source")
        contents = soup.select(".contson")
        for i in range(len(titles)):
            item = {}
            item['title'] = titles[i].string
            item['author'] = authors[i].get_text()
            item["content"] = contents[i].get_text().replace("\n","")
            # print(item)
            items.append(item)
    elif type == 'm':
        mingju = soup.select(".sons .cont")
        for i in range(len(mingju)):
            item = {}
            item['content'] = mingju[i].select('a')[0].string
            item['author'] = mingju[i].select('a')[1].string
            items.append(item)
    elif type == "a":
        img = soup.select(".cont .divimg a img")
        authors = soup.select(".sonspic .cont")
        for i in range(len(img)):
            item = {}
            item['img_url'] = img[i].attrs['src']
            item['author'] = authors[i].select('a')[1].string
            items.append(item)
    else:
        book_name = soup.select(".sonspic .cont")
        # print(book_name)
        for i in book_name:
            item = {}
            item['name'] = i.select('a')[1].string
            items.append(item)
    with open('a.json', 'ab+')as f:
        for data in items:
            str_data = json.dumps(data, ensure_ascii=False) + ',\n'
            f.write(str_data.encode())