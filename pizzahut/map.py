# -*- coding:utf-8 -*-
import json
import demjson
from pyecharts import Geo


def get_city_name():
    cities = []
    file_name = 'cities.txt'
    with open(file_name, 'r', encoding="UTF-8") as file:
        for line in file:
            city = line.replace('\n', '')
            cities.append(city)
        return cities


def get_data(cities):
    file_name = 'results.json'
    data = []
    with open(file_name,  'r', encoding="UTF-8-sig") as load_f:
        load_dict = json.load(load_f)
        for city in cities:
            #print(city)
            count_restaurants = len(load_dict[city])
            city_restaurant = (city, count_restaurants)
            data.append(city_restaurant)
        #print(data)
        return data


def get_map(data):
    print(data)
    geo = Geo(
        "全国必胜客城市分布",
        "data from pizzahut",
        title_color="#fff",
        title_pos="center",
        width=1200,
        height=600,
        background_color="#404a59",
    )
    try:
        attr, value = geo.cast(data)
        geo.add(
            "",
            attr,
            value,
            visual_range=[0, 200],
            visual_text_color="#fff",
            symbol_size=10,
            is_roam=True,
            is_visualmap=True,
        )
        geo.render()
    except ValueError as info:
        error_city = str(info).split(' ')[-1]
        print(error_city)
        dict = {k: v for k, v in data}
        print((error_city, dict[error_city]))
        data.remove((error_city, dict[error_city]))
        get_map(data=data)


if __name__ == '__main__':
    cities = get_city_name()
    data = get_data(cities)
    get_map(data=data)
    # list = [('潍坊', 9), ('钦州', 1), ('库尔勒', 2)]
    # dict = {k: v for k, v in list}
    # print(list.index(('潍坊', dict['潍坊'])))


