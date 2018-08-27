import requests
from urllib import request
import re
import selenium.webdriver
import time
import os
import random

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"}
url = "http://ac.qq.com"

# js语句，让一个页面分10次加载，直至加载整个页面
def scorll(n,i):
    return "window.scrollTo(0,(document.body.scrollHeight/{0})*{1}*30);".format(n, i)

# 控制selenium的部分，获取整个页面的内容
def get_ac(url):
    driver = selenium.webdriver.Chrome()
    driver.get(url)
    n = 10
    for i in range(0,n+1):
        # 调用scoll函数
        s = scorll(n,i)
        # 在谷歌浏览器里执行js语句
        driver.execute_script(s)
        # 随机停止一段时间，模拟人看浏览器
        time.sleep(random.randint(2,5))
    # 获得整个页面的文本
    content = driver.page_source
    # 关闭当前界面，不关会一直开启新页面
    driver.quit()
    return content

def get_img():
    urll = "http://ac.qq.com/Comic/ComicInfo/id/531490"
    driver = selenium.webdriver.Chrome()
    driver.get(urll)
    content = driver.page_source
    driver.quit()
    ss = '<a target="_blank" title="一人之下(.*?)>'
    title_name = re.compile(ss).findall(content)
    # print(title_name)
    for li in title_name:
        url_f = url+li.split('"')[2]
        print(url_f)
        html = get_ac(url_f)
        # print(html)
        zz = 'img src="(https://.*?.jpg/0)"'
        title = 'span class="title-comicHeading">(.*?)</span>'
        # 图片地址列表
        img_url = re.compile(zz).findall(html)
        # 章节名字列表
        title_name = re.compile(title).findall(html)
        print(img_url)
        print(title_name)
        # zzz = 'img src="(https:.*?&)amp;(.*?)amp;(dir_path=/&)amp;(.*?.jpg)'
        # img_url1 = re.compile(zz).findall(html)
        # print(img_url1)
        n = 1
        for i in img_url:
            filename = 'E:/img/'+str(title_name[0])
            is_exist = os.path.exists(filename)
            if not is_exist:
                os.makedirs((filename))
                print(filename + "创建成功")
            reqimg = request.Request(i, headers=headers)
            img = request.urlopen(reqimg)
            photo = img.read()
            file = open(filename+"/"+str(n)+'.jpg', "wb")
            file.write(photo)
            print("正在下载")
            n += 1

if __name__ == '__main__':
    get_img()