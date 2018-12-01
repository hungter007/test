from datetime import datetime, timedelta
import time
import requests
from pyecharts import Geo
import json
urls = 'http://m.maoyan.com/mmdb/comments/movie/1208282.json?_v_=yes&offset=15&startTime=2018-11-30%2010%3A12%3A15'
file_name = 'comments.txt'

def get_data(url):
    headers = {
        'User-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko)\
         Version/11.0 Mobile/15A372 Safari/604.1'
    }
    html = requests.get(url=url, headers=headers)
    if html.status_code == 200:
        return html.content
    else:
        return None


def parse_data(html):
    json_data = json.loads(html)['cmts']
    comments = []
    try:
        for item in json_data:
            comment = {
                'nickName': item['nickName'],
                'cityName': item['cityName'] if 'cityName' in item else '',
                'content': item['content'].strip().replace('\n',''),
                'score': item['score'],
                'startTime': item['startTime']
            }
            comments.append(comment)
        return comments
    except Exception as e:
        print(e)


def save():
    start_time = '2018-11-24 21:00:42'
    end_time = '2018-11-16 00:00:00'
    while start_time > end_time:
        url = 'http://m.maoyan.com/mmdb/comments/movie/1208282.json?_v_=yes&offset=15&startTime=' + start_time.replace(
            ' ', '%20')
        print(url)
        try:
            html = get_data(url=url)
        except Exception as e:
            print(e)
            time.sleep(3)
            html = get_data(url)
        else:
            time.sleep(5)
        comments = parse_data(html)
        start_time = comments[14]['startTime']
        print(start_time)
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=-1)
        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')
        for item in comments:
            with open(file_name, 'a+', encoding='utf-8') as f:
                f.write(item['nickName']+','+item['cityName'] + ','+item['content']+','+str(item['score'])+','
                        + item['startTime'] + '\n')


def get_cities_data():
    cities = {}
    with open(file_name, 'r', encoding='utf-8') as f:
        row_data = f.readlines()
        try:
            for data in row_data:
                    city = data.split(',')[1]
                    if city and '\u4e00' <= city <= '\u9fff':
                        if city in cities:
                            cities[city] += 1
                        else:
                            cities[city] = 1
            # print(cities)
        except Exception as e:
            print(e)
        return cities


def create_map(data):
    geo = Geo('《无名之辈》观众位置分布', '数据来源：猫眼采集',
              title_color="#fff",
              title_pos="center",
              width=1200,
              height=600,
              background_color="#404a59")
    try:
        attr, value = geo.cast(data)
        geo.add(
            "",
            attr,
            value,
            visual_range=[0, 1000],
            visual_text_color="#fff",
            symbol_size=15,
            is_visualmap=True,
        )
        geo.render("观众位置分布-地理坐标图.html")
    except ValueError as info:
        error_city = str(info).split(' ')[-1]
        del data[error_city]
        create_map(data)
    data_top20 = 



if __name__ == '__main__':
    #获取数据
    #save()
    cities_data = get_cities_data()
    create_map(cities_data)

