import csv
import json
from urllib import request,parse
from lxml import etree
from selenium import webdriver
import time

# 定义一个爬虫类
class ZhilianSpider(object):
    # 重写构造方法
    def __init__(self,city,start,job,end,url):
        self.city = city
        self.start = start
        self.job = job
        self.end = end
        self.url = url
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"}



    # 定义一个成员方法
    def hand_url(self,page):
        # 给地点改成ascii码
        name = {
            "jl": city
        }
        data = parse.urlencode(name)
        # print(data)
        self.url = url+"p="+str(page)+data+"&kw="+job+"&kt=3"
        # print(self.url)
        return self.url

    # 处理请求
    def request_jobs(self,req):
        # content = request.urlopen(req).read().decode("utf-8")
        # print(content)

        driver = webdriver.Chrome()
        driver.get(req)
        time.sleep(2)
        content = driver.page_source
        driver.quit()

        # 带s的获取多个元素，返回的是list数列
        # element定位的是单数，直接定位到元素
        # self.driver.find_elements_by_class_name("btn btn-pager")[1].click()

        return content

    # 解析并存储
    def analysis(self,content):
        data = []
        html_tree = etree.HTML(content)
        tmp = {}
        job_list = html_tree.xpath("//div[@class='itemBox nameBox']/div/a/span/@title")
        salary_list = html_tree.xpath("//div[@class='itemBox descBox']/div/p/text()")
        company_list = html_tree.xpath("//div[@class='itemBox nameBox']/div/a/@title")
        area_list = html_tree.xpath("//div[@class='itemBox descBox']/div/ul/li[1]/text()")
        experice_list = html_tree.xpath("//div[@class='itemBox descBox']/div/ul/li[2]/text()")
        # xueli_list = html_tree.xpath("//div[@class='itemBox descBox']div[1]/ul/li[3]/text()")
        tmp["职位"] = job_list
        tmp["薪水"] = salary_list
        tmp["公司"] = company_list
        tmp["地区"] = area_list
        tmp["工作经验"] = experice_list
        # tmp["学历"] = xueli_list
        data.append(tmp)
        # print(data)
        return data

    # 存储
    def save_data(self,data):
        for k in data:
            job = k.get("职位")
            salary = k.get("薪水")
            company = k.get("公司")
            area = k.get("地区")
            experience = k.get("工作经验")
            for i in range(60):
                h = job[i].replace("\xa0","")
                print(h)
                with open(r"C:\Users\DELL\Desktop\zhilian.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([h, salary[i], company[i],area[i],experience[i]])

    # 封装一个函数作为对外接口

    def start_crawl(self):
        with open(r"C:\Users\DELL\Desktop\zhilian.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["职位", "薪水", "公司", "地区", "工作经验"])
        # 遍历所有的页面
        for i in range(int(self.start),int(self.end)+1):
            # 请求对象
            req = self.hand_url(i)
            # 发起请求
            html = self.request_jobs(req)
            # print(html)
            # 解析
            items = self.analysis(html)
            # 存储数据
            self.save_data(items)
            print("保存完毕")


if __name__ == '__main__':
    url = "http://sou.zhaopin.com/jobs/searchresult.ashx?"
    #p=3&jl=北京&kw=python
    city = input("请输入工作城市：")
    job = input("请输入岗位：")
    start = input("请输入起始页：")
    end = input("请输入终止页：")
    # 创建一个爬虫对象
    zhi = ZhilianSpider(end=end,start=start,job=job,city=city,url=url)
    zhi.start_crawl()
