import json
import threading
import time

import requests
from bs4 import BeautifulSoup


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"}

def parse_first_page(url):
    r = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    number_list = soup.select(".bus_kt_r1 > a")
    # print(number_list)
    char_list = soup.select(".bus_kt_r2 a")
    # print(char_list)
    all_list = number_list + char_list
    # print(all_list)
    href_list = []
    for i in all_list:
        # rstrip是删除指定字符串末尾的某个字符
        url_1 = url.rstrip("/") + i['href']
        href_list.append(url_1)
    return href_list

def parse_second_page(href,url):
    r = requests.get(url=href,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    a_list = soup.select("#con_site_1 > a")
    # print(a_list)
    href_list = []
    for i in a_list:
        href_list.append(url.rstrip("/") + i['href'])
    return href_list
def parse_third_page(href,f):

    r = requests.get(url=href, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    name = soup.select('.bus_i_t1 > h1')[0].get_text()
    run_time = soup.select('.bus_i_content > p')[0].get_text()
    # print(run_time)
    price_info = soup.select('.bus_i_content > p')[1].get_text()
    company = soup.select('.bus_i_content > p > a')[0].get_text()
    update_time = soup.select('.bus_i_content > p')[3].get_text()
    # 获取全程总长
    try:
        route_bus = soup.select('.bus_label > p')[0].get_text()
    except:
        route_bus="空空如也"
    # 上行站牌数
    up_number = soup.find_all("span",class_='bus_line_no')[0].get_text().replace("\xa0","")
    # print(up_number)
    # 站牌名字
    up_list = []
    up_site = soup.select(".bus_line_site")[0].find_all("a")
    # 列表生成式
    [up_list.append(i.get_text()) for i in up_site]
    # print(len(up_list))
    # exit()
    # 下行站牌数
    try:
        down_number = soup.find_all("span", class_='bus_line_no')[1].get_text().replace("\xa0", "")
        # print(down_number)
        # 站牌名字
        down_list = []
        down_site = soup.select(".bus_line_site")[1].find_all("a")
        # print(len(down_site))
        [down_list.append(j.get_text()) for j in down_site]
        # print(down_list)
        # exit()
    except:
        down_number = "空"
        down_list = []
    items = {
        "线路名称":name,
        "运行时间":run_time,
        "价格信息":price_info,
        "公交公司":company,
        "更新时间":update_time,
        "全程总长":route_bus,
        "上行站牌数":up_number,
        "上行站台":up_list,
        "下行站牌数":down_number,
        "下行站台":down_list
    }
    # print(items)
    bus_json = json.dumps(items, ensure_ascii=False)+"\n"
    # print(bus_json
    f.write(bus_json)
    print("以爬取：%s"%name)

def main():
    url = "http://beijing.8684.cn/"
    with open("beijing_bus_station.json","w",encoding="utf-8") as f:
        # 处理一级页面
        bus_href_list = parse_first_page(url)
        # 处理二级页面
        for bus_href in bus_href_list:
            href_list = parse_second_page(bus_href,url=url)
            # print(href_list)
            for href in href_list:
                parse_third_page(href,f)
        f.close()


if __name__ == '__main__':
    main()

