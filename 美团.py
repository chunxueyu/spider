import requests
import re
import json
from bs4 import BeautifulSoup
from urllib import request
import csv


url = "http://bj.meituan.com/meishi/"
headers = {
    'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'Accept-Encoding':' gzip, deflate',
'Accept-Language':' zh-CN,zh;q=0.9',
# 'Connection':' keep-alive',
'Cookie':' _lxsdk_cuid=16509a8a7dbc8-0ffaefc2fbed5b-2711639-144000-16509a8a7ddc8; __mta=46078747.1533465372655.1533601994261.1533602061951.5; iuuid=04CA67C6A4DB81A68AC3901617C50E8C0CC55B8C885891CDB87E73198AC1899C; cityname=%E9%82%B9%E5%B9%B3; _lxsdk=04CA67C6A4DB81A68AC3901617C50E8C0CC55B8C885891CDB87E73198AC1899C; ci=1; rvct=1%2C238%2C508%2C197%2C88; uuid=34b3e0f7b4634b4680bb.1537952958.1.0.0; client-id=38190958-dce4-463f-843f-267d2e97160b; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; lat=39.997991; lng=116.488551; _lxsdk_s=166157c8b62-7d3-ea7-1e1%7C%7C51',
'Host':' www.meituan.com',
'Referer': 'http://bj.meituan.com/meishi/pn1/',
'Upgrade-Insecure-Requests':' 1',
'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Mobile Safari/537.36'}

with open("meituan.csv","w" ,newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["名字","评分","地址","联系电话","营业时间","人均价格"])

    for k in range(33):
        k_url = url + "pn" + str(k) + "/"
        r = requests.get(k_url)

        zz = '"poiInfos":(.*)},"comHeader"'
        pattern = re.compile(zz)
        ret = pattern.findall(r.text)[0]
        hehe = json.loads(ret)
        for i in hehe:
            # print(i["poiId"])
            new_url = "http://www.meituan.com/meishi/"+ str(i["poiId"]) + "/"
            req = request.Request(url=new_url, headers=headers)
            resp = request.urlopen(req)
            aaa = resp.read().decode("utf-8").replace("\u2022","").replace("\xe2","")
            gg = '({"poiId".*?),"photos"'
            pattern_2 = re.compile(gg)
            re_f = pattern_2.findall(aaa)[0]
            print(re_f)

            # hh = json.loads(re_f)
            # print(hh["name"])
            # exit()

            # 无限正则大法
            name = re.compile('"name":"(.*?)"').findall(re_f)[0]
            avgScore = re.compile('"avgScore":(.*?),').findall(re_f)[0]
            address = re.compile('"address":"(.*?)"').findall(re_f)[0]
            phone = re.compile('"phone":"(.*?)"').findall(re_f)[0]
            openTime = re.compile('"openTime":"(.*?)"').findall(re_f)[0]
            avgPrice = re.compile('"avgPrice":(.*?),').findall(re_f)[0]

            print(name)
            writer.writerow([name, avgScore, address, phone, openTime,avgPrice])
f.close()