# -*- coding:utf-8 -*-
from urllib.parse import quote
from lxml import etree
from bs4 import BeautifulSoup

import json
import requests
import time

url = 'http://www.pizzahut.com.cn/'

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/69.0.3497.92 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'www.pizzahut.com.cn',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

cities = []


def get_cities_fromhtml():
    """从html中获取地址"""
    session = requests.Session()
    resp = session.get(url=url, headers=headers)
    html1 = etree.HTML(resp.text)

    cities = html1.xpath("//div[@class='this_f_letters']/a/text()")
    cities = list(set(cities))
    print(cities)
    with open('cities.txt', 'w', encoding="UTF-8") as file:
        for city in cities:
            file.write(city+'\n')
    return city

def get_cities_fromfile():
    """从文件中读取地址"""
    file_name = 'cities.txt'
    with open(file_name, 'r', encoding="UTF-8-sig") as file:
        for line in file:
            city = line.replace('\n', '')
            cities.append(city)

    count = 1
    results = {}
    #遍历所有城市餐厅
    for city in cities:
        restaurants = get_stores(city, count)
        results[city] = restaurants
        count += 1
        time.sleep(2)

    with open('results.json', 'w', encoding='UTF-8') as file:
        file.write(json.dumps(results, indent=4, ensure_ascii=False))


def get_stores(city, count):
    session = requests.Session()
    city_urlencode = quote(city+'|0|0')
    print(city_urlencode)
    cookies = requests.cookies.RequestsCookieJar()

    print('============第', count, '个城市:', city, '============')
    resp = session.get(url=url, headers=headers)
    cookies.set('AlteonP', resp.cookies['AlteonP'], domain='www.pizzahut.com.cn')
    cookies.set('iplocation', city_urlencode, domain='www.pizzahut.com.cn')
    print(cookies)

    page = 1
    restaurants = []

    while True:
        data = {
            'pageIndex': page,
            'pageSize': "30"
        }
        response = session.post('http://www.pizzahut.com.cn/StoreList/Index', cookies=cookies, headers=headers, data=data)
        html = etree.HTML(response.text)
        temp_items = []
        divs = html.xpath("//div[@class='re_RNew']/@onclick")
        for div in divs:
            item = {}
            content = div.split('(\'')[1].split("\',\'")[0]
            if len(content.split('|')) == 4:
                item['coordinate'] = content.split('|')[0]
                item['restaurant_name'] = content.split('|')[1] + '店'
                item['address'] = content.split('|')[2]
                item['phone'] = content.split('|')[3]
            else:
                item['restaurant_name'] = content.split('|')[0] + '店'
                item['address'] = content.split('|')[1]
                item['phone'] = content.split('|')[2]
            temp_items.append(item)
            print(item)
        if not temp_items:
            break
        restaurants += temp_items
        page += 1
        time.sleep(3)
    return restaurants


if __name__ == '__main__':
    get_cities_fromfile()
    # items = ["ClickStore('23.063612,113.391719|中环东路|小谷围街中二横路1号高高新天地商业广场B栋一层B1A005、B1A006和二层B2A001、B2A002|020-31141049','GZ2526')", "ClickStore('22.794546,113.530925|南沙万达|道办环市大道中南沙万达广场南A1区1层1026房|020-39012954','GZ2544')", "ClickStore('23.276926,113.814513|增城万达|荔城街增城大道69号万达广场一层1001，二层2001|020-32178317','GZ1824')", "ClickStore('23.101124,113.453349|黄埔东路|黄埔东路168号一层104铺自编102房|020-82509872','GZ1574')", "ClickStore('23.139173,113.287538|淘金路|淘金坑路28号之一层至四层|020-83489539','GZ1557')", "ClickStore('23.028942,113.330389|星河湾|大石镇迎宾路星河湾四季会会所首层|020-34792399','GZ1819')", "ClickStore('23.127819,113.602263|港口大道|新塘镇港口大道332号金海岸广场首层|020-32177071','GZ2563')", "ClickStore('23.007498,113.350362|番禺万达|南村镇兴南大道368号万达广场内1030、2036号商铺|020-31054090','GZ1821')", "ClickStore('23.15148138,113.35429341|五山HS|茶山路251-261（单号）号首层自编108号|020-38857290','GZH757')", "ClickStore('23.169724,113.467174|萝岗万达|科丰路89号万达广场首层1028.2029.2030号铺|020-82006534','GZ2522')", "ClickStore('23.089603,113.276606|昌岗苏宁|昌岗中路238号负一层自编7号|020-89202715','GZ1504')", "ClickStore('23.39796,113.233153|花都广百|新华街龙珠路41号广百新一城花都购物广场二层|020-37712065','GZ1506')", "ClickStore('22.924089,113.358099|奥园|南华路奥园广场二层|020-31079453','GZ1507')", "ClickStore('23.092852,113.29082|中大科技园|新港西路135号中山大学（南校区）蒲园区628号中大科技综合楼B座首二层|020-34479745','GZ1513')", "ClickStore('22.799422,113.556109|华汇广场|近郊进港大道4号华汇国际广场首层|020-31154123','GZ1516')", "ClickStore('23.128737,113.297045|农林下路|农林下路37号美东百货二层|020-87780029','GZ1523')", "ClickStore('23.194609,113.261884|百信广场|机场路1309号百信广场5楼|020-36637408','GZ1524')", "ClickStore('23.132746,113.326686|正佳|天河路228号正佳广场三层|020-38330151','GZ1525')", "ClickStore('23.158296,113.234505|骏盈|同康路骏盈广场2层|020-36478289','GZ1526')", "ClickStore('23.335243,113.295363|人和站|人和镇人和墟106国道旁维也纳酒店鹤龙路189号|020-36770643','GZ1534')", "ClickStore('23.026277,113.310983|富丽|大石街105国道大石段257，259号，大石富丽城一层+二层|020-34799466','GZ1537')", "ClickStore('23.095697,113.230037|百花路|百花路8号花地人家商业中心商业区首层自编102，二层自编201|020-81552723','GZ1543')", "ClickStore('23.110638,113.23931|西城都荟|黄沙大道8号广州西城都荟广场第一层106-107铺|020-81293960','GZ1560')", "ClickStore('23.115575,113.420334|乐都汇|东圃珠村中山大道1116号乐都汇购物中心一层|020-32394167','GZ1562')", "ClickStore('23.12606,113.574525|凤凰城|凤妍苑步行街（南）1号101商铺一楼|020-32162870','GZ1565')", "ClickStore('23.089199,113.259506|乐峰|工业大道北乐峰广场负首二层|020-89308251','GZ1566')", "ClickStore('23.072944,113.292329|海珠新都荟|东晓南路1290号101房自编1-A02铺，201房自编2A06铺|020-84151591','GZ1567')", "ClickStore('23.134389,113.284993|宜安|建设六马路33号宜安广场二楼|020-83633120','GZH508')", "ClickStore('23.131736,113.306648|东峻|东风东路836号东峻广场首层|020-87679903','GZH517')", "ClickStore('23.125462,113.378528|棠下|中山大道188号好又多美食广场首、二层|020-85530977','GZH523')", "ClickStore('23.141635,113.340059|天河北万佳|天河北路607号天河北万佳百货首层|020-38473048','GZH524')", "ClickStore('23.132709,113.322616|天河城|天河路208号天河城广场七楼|020-85585008','GZH537')", "ClickStore('23.095787,113.319409|丽影|新港中路352号之一至三丽影商业广场首层二层|020-34398001','GZH555')", "ClickStore('23.113454,113.242097|十甫|第十甫路12号首层+二层|020-81712180','GZH559')", "ClickStore('23.133169,113.320941|中怡|天河路200号广百中怡时尚坊负一层、负二层|020-85598180','GZH560')", "ClickStore('23.181339,113.321114|佳润|广州大道北1419号佳润广场首、二层|020-87276822','GZH572')", "ClickStore('23.400593,113.217602|花都百业|新华镇公益路百业广场首二层|020-86895050','GZH574')", "ClickStore('23.042108,113.37206|大学城|大学城大学生活区商业中心一层|020-39337159','GZH575')", "ClickStore('23.147105,113.325082|天汇城|林和中路63号广州东方宝泰购物广场首层|020-38096186','GZH579')", "ClickStore('23.123043,113.269514|名盛|北京路238号名盛广场五层|020-83179844','GZH585')", "ClickStore('23.125102,113.255571|中六乐购|中山六路285号-287号越秀上品轩首层负一层|020-81306066','GZH592')", "ClickStore('22.948795,113.362484|富华|富华西路2号钻汇广场一层|020-39994528','GZH803')", "ClickStore('23.173476,113.267612|万达|云城东路509号万达商业广场室内步行街一层|020-36689199','GZH804')", "ClickStore('23.155156,113.264015|机场路|机场路12号二层|020-36682012','GZH811')", "ClickStore('23.283108,113.817561|增城广场|荔城街府佑路98号，第1106号东汇城商铺首、二层|020-26251021','GZH813')", "ClickStore('23.125673,113.233974|中山八|中山八路64号首层|020-81812814','GZH814')", "ClickStore('23.120333,113.402511|东圃四季|东圃大马路4号D栋首、二层|020-82165587','GZH820')", "ClickStore('23.180767,113.265934|云城西|机场路云霄街353幢五号停机坪购物广场一层|020-36079677','GZH830')", "ClickStore('23.45557,113.172552|狮岭宝峰|狮岭镇宝峰路2号狮岭宝峰皮具材料城之首二层|020-37718501','GZH833')", "ClickStore('23.120274,113.321722|珠江新城|珠江新城花城大道85、87号高德置地春广场负一、负二层|020-38838171','GZH839')"]
    # for item in items:
    #     needs = item.split('(\'')[1].split("\',\'")[0]
    #     print(needs)
