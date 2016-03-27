#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2016-03-27 16:41:11

import datetime, requests, time, json

URL = 'http://train.qunar.com/qunar/checiInfo.jsp'
DEFAULT_DATE = datetime.datetime.now() + datetime.timedelta(30,0,0)
DEFAULT_DATE_STR = DEFAULT_DATE.strftime('%Y-%m-%d') # 默认查询30天后的时刻表
def getinfo(train_number = 'G76', date=DEFAULT_DATE_STR):
    ''' 输入: 高铁班次: G11， 
              日期: '2016-04-30';
        输出: {
            'train_number':'G1',
            'date': '2016-04-21',
            'schedule': [
                ["站次","站名","到达时间", "开车时间","停车时间","里程"]
                    # 起始站的到达时间， 终点站的开车时间， 二者的停车时间都为 "-"
                [],  # 第一个数据是起始站
                [],  # 中间的数据是停靠站
                [],  # 中间的数据是停靠站
                [],  # 中间的数据是停靠站
                ,...,
                [],  # 最后一个数据是终点站
            ]
        }
    '''
    params = {
        'method_name': 'buy',
        'ex_track': '',
        'q': train_number,
        'date': date.replace('-',''),
        'format': 'json',
        'cityname': 123456,
        'ver': int(time.time()*1000),
    }
    url = URL
    response = requests.get(url=url,params=params,
            headers={'Content-Type':'application/json'})
    return json.loads(response.text)

def test():
    print(getinfo())

if __name__ == '__main__':
    test()
