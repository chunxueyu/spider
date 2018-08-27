import requests
from lxml import etree
s = requests.Session()
for id in range(0,101,25):
    url = "https://www.douban.com/doulist/45004834/?start="+str(id)
    #print(url)
    r = s.get(url)
    r.encoding = 'utf-8'
    root = etree.HTML(r.content)
    items = root.xpath('//*[@class="bd doulist-subject"]')
    #print(len(items))
    for item in items:
            title = item.xpath('//*[@class="doulist-item"]/div/div[2]/div[3]/a/text()')
            #print(title)
            for text in title:
                with open('C:\\Users\\DELL\\Desktop\\xiaoshuo.txt','a') as f:
                    f.write(text.replace(" ","").replace("\n",""))
                    print("正在写入")
                    f.write("\r\n")  # 换行写入
    f.close()