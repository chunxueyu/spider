from urllib import request,parse
from lxml import etree
from selenium import webdriver
from time import sleep
# from write_mysql import inser_msg

class ZhilianSpider(object):
    #重写构造方法
    def __init__(self,area,job,end,start):
        self.area = area
        self.job = job
        self.end = end
        self.start = start
        self.url = "https://sou.zhaopin.com/?&pageSize=60&jl={city}&kw={job}&kt=3".format(
            city = area,
            job = job
        )
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
        }
        self.driver = webdriver.Chrome()
        # 请求首页
        self.driver.get(self.url)

    # 处理请求
    def request_job(self):
        sleep(1)
        # 对起始页面进行判断
        print(self.start)
        if int(self.start) <= 1:
            self.start = 1
            self.driver.find_elements_by_class_name("btn-pager")[1].click()
            print('start小于1')
        else:
            for i in range(1,int(self.start)):
                print('start大于1')
                self.driver.find_elements_by_class_name("btn-pager")[1].click()
                # 获取网页源码

                # print(html)
        sleep(1)
        # self.driver.find_elements_by_class_name("btn-pager")[1].click()
        html = self.driver.page_source
        return html
    # 解析
    def analysis_req(self,html):
        html_etree = etree.HTML(html)
        job_path = html_etree.xpath("//div[@class='infoBox']")
        job_list = []
        for job in job_path:
            tmp = {}
            position = job.xpath(".//span[@class='job_title']/@title")[0]
            company = job.xpath(".//a[@class='company_title']/text()")[0]
            salary = job.xpath(".//p[@class='job_saray']/text()")[0]
            model = job.xpath(".//span[@class='info_item']/text()")[0]
            tmp["position"] = position
            tmp["company"] = company
            tmp["salary"] = salary
            tmp["model"] = model
            job_list.append(tmp)
        return job_list
        # position =
        # print(position)
        # msg_dict["position"] = position
        # print(msg_dict)

        # msg_dict = [dict(zip(["位置"],i)) for i in position]
        # staff = html_etree.xpath("//div[starts-with(@class,'listItemBox-wrapper')]//span[@class='info_item']/text()")
        # print(staff)
        # return position
    #存储
    def save_msg(self,content):
        pass


    def start_crawl(self):
        #遍历所有页面
        page_all = []
        for i in range(1,int(self.end)+1):
            # 请求对象
            # req = self.handl_url(page=i)
            # 发起请求
            html = self.request_job()
            #解析
            items = self.analysis_req(html)
            print(items)
            # for i in items:
                # res = inser_msg(i)
                # print(res)

            #存储数据
            page_all += items
        self.driver.quit()


if __name__ == '__main__':
    # url = "https://sou.zhaopin.com/jobs/searchresult.ashx?"
    city = input("请输入工作城市:")
    job = input("请输入心仪岗位:")
    start = input("请输入起始页面:")
    end = input("请输入结束页面:")
    #创建一个爬虫对象
    zhi = ZhilianSpider(area = city,job = job,end = end,start = start)
    zhi.start_crawl()


