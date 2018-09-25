import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"}

# 反爬：token动态生成， post接口有动态的get参数

# 请求登录页
login_page_url = "http://bbs.chinaunix.net/member.php?mod=logging&action=login&logsubmit=yes"


# 创建一个session对象
s = requests.Session()
login_page = s.get(url=login_page_url,headers=headers)
soup = BeautifulSoup(login_page.text,'lxml')
# print(soup)
# 获取token值
formhash = soup.select("[name='formhash']")[0].attrs.get("value")
referer = soup.select("[name='referer']")[0].attrs.get("value")
# 构造请求体
data = {
    "formhash":formhash,
    "referer":referer,
    "return_type":'',
    "loginsubmit":"true",
    "username":"MrFan666",
    "password":"f12345678"
}

# 登录
# 获取登陆接口
params = soup.select("form.cl")[0].attrs.get("action")
print(params)
login_url = "http://bbs.chinaunix.net/" + params
print(login_url)

# 发起post请求
res = s.post(url=login_url,data=data,headers=headers)
print(res.text)

