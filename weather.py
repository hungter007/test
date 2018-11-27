# -*- coding:utf-8 -*-

from lxml import etree

import json
import requests
import time
import re

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/69.0.3497.92 Safari/537.36'
}


def get_cities():
    url = 'http://www.tianqihoubao.com/aqi'
    response = requests.get(url, headers=headers)
    pattern = re.compile('href="/aqi/(.*?).html')
    items = re.findall(pattern, response.text)
    items = list(set(items))
    return items


def get_weather_data(city):

    for month in range(1, 13):
        print('============城市', city, ':', month, '月============')
        time.sleep(5)
        url = 'http://www.tianqihoubao.com/aqi/' + city + '-2018' + str("%02d" % month) + '.html'
        session = requests.Session()
        response = session.get(url=url, headers=headers)
        html = etree.HTML(response.text)
        for day in range(2, 33):
            weather_data = html.xpath("//div[@class='api_month_list']/table/tr[%d]/td/text()" % day)
            print(weather_data)
            if weather_data:
                date = weather_data[0].strip()
                quality_grade = weather_data[1].strip()
                aqi = weather_data[2].strip()
                aqi_rank = weather_data[3]
                pm2_5 = weather_data[4]
                pm10 = weather_data[5]
                so2 = weather_data[5]
                no2 = weather_data[5]
                co = weather_data[5]
                o3 = weather_data[5]
                filename = 'air_' + city + '_2018.csv'
                with open(filename, 'a+', encoding="utf-8-sig") as f:
                    f.write(date + ',' + quality_grade + ',' + aqi + ',' + aqi_rank + ',' + pm2_5 + ',' + pm10 + ',' +
                            so2 + ',' + no2 + ',' + co + ',' + o3 + '\n')


if __name__ == '__main__':
    city = 'guangzhou'
    cities = get_cities()
    for city in cities:
        get_weather_data(city)
        time.sleep(4)
