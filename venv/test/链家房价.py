from urllib import request
from bs4 import BeautifulSoup
import threading
import re
import csv    #导入表格的包
import time

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"}

def getHtml(url):
    req = request. Request(url,headers=headers)
    response = request.urlopen(req)
    html = response.read()
    return html.decode("utf-8")
    #print(html)

def getAllEle(a,b):
  for i in range(a,b):
      url = "https://bj.fang.lianjia.com/loupan/pg" + str(i) + "/"
      # getHtml(url)
      soup = BeautifulSoup(getHtml(url), 'html.parser')
      liList = soup.find('ul', class_='resblock-list-wrapper').find_all('li')
      # print(liList)
      for i in liList:
          # print(i)
          # 小区名
          re_name = re.compile(r'<a class="name".*?target="_blank">(.*?)</a>', re.S)
          name1 = re_name.findall(str(i))
          name = name1[0]
          print(name)
          # 小区位置
          re_address = re.compile(r'<a data.*?target="_blank">(.*?)</a>', re.S)
          address1 = re_address.findall(str(i))
          address = address1[0]
          print(address)
          try:
              # 单价数字
              re_price = re.compile(r'<span class="number">(.*?)</span>', re.S)
              price1 = re_price.findall(str(i))
              price = price1[0]
              # 单价单位
              re_danwei = re.compile(r'<span class="desc">(.*?)</span>', re.S)
              danwei1 = re_danwei.findall(str(i))
              danwei = danwei1[0].replace('\xa0', '')
              Price = price + danwei
              print(Price)
          except IndexError as e:
              Price = "价格待定"
              print(Price)
          with open(r"C:\Users\DELL\Desktop\house.csv","a",newline="") as f:  #加入newline=""就不会换行了
              writer = csv.writer(f)
              writer.writerow([name,address,Price])
  f.close()


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

if __name__ == "__main__":
    with open(r"C:\Users\DELL\Desktop\house.csv", "a",newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["小区","详细地址","价格"])
    th1 = MyThread(getAllEle,1,15)
    th2 = MyThread(getAllEle, 16, 32)
    th3 = MyThread(getAllEle, 33, 52)
    th1.start()
    time.sleep(1)
    th2.start()
    time.sleep(1)
    th3.start()

#使用suop直接获得多个文本
# li = soup.find('div', class_='resblock-desc-wrapper').find_all('a')
      # name = li[0].get_text()
      # address = li[1].get_text()
      # name = soup.find('div', class_='resblock-name').find('a').get_text()
      # address = soup.find('div', class_='resblock-location').find('a').get_text()
      # print(name, address)
      #
      # sell = soup.find('div',class_='resblock-price').find_all('span')
      # try:
      #     price = sell[0].get_text()+sell[1].get_text()
      #     print(price)
      # except IndexError as e:
      #     price = "价格待定"
      #     print(price)


#试图把数据写入一个列表，再从列表中取得数据，失败
# class Intial:
#     def __init__(self,name,address,Price):
#         self.name = name
#         self.address = address
#         self.Price = Price
# class Addlist:
#     List = []
#     def add_list(self):
#         d1 = ("小区", "详细地址", '价格')
#         Addlist.List.append(d1)
# b = Intial(name, address, Price)
# Addlist.List.append(b)
# print(Addlist.List[1][0])
# suib()
# c = Addlist()
# c.add_list()
# with open(r"C:\Users\DELL\Desktop\house.csv", "a") as f:
#     writer = csv.writer(f)
#     for n in Addlist.List:
#         writer.writerow([n[0], n[1], n[2]])
#     f.close()