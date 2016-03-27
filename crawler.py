#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2016-03-27 16:41:11

import datetime, requests, time, json, logging

from requests.exceptions import Timeout

URL = 'http://train.qunar.com/qunar/checiInfo.jsp'
DEFAULT_DATE = datetime.datetime.now() + datetime.timedelta(30,0,0)
DEFAULT_DATE_STR = DEFAULT_DATE.strftime('%Y-%m-%d') # 默认查询30天后的时刻表

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='./log/crawler.log',
                filemode='a')

def getinfo(train_number = 'G99', date=DEFAULT_DATE_STR):
    ''' 输入: 高铁班次: G11， 
              日期: '2016-04-30';
        输出: { # 输出格式暂时不修改, 
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
    logging.info('getinfo')
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
    try: 
        response = requests.get(url=url,params=params,
                headers={'Content-Type':'application/json'}, timeout=10)
    except Timeout:
        logging.error('无法从服务器获取数据')
        logging.error('url: '+url)
        logging.error(params)
        return None
    result = json.loads(response.text)
    if result== {'count':'0'}:
        trainfile = open('./data/不存在的火车车次','a')
        trainfile.write(train_number+'\n')
        trainfile.close()
        return None
    return response.text

def main():
    for i in range(1,9730):
        time.sleep(5)
        train = 'G' + str(i)
        result = getinfo(train_number = train)
        if result:
            gotfile = open('./data/火车班次json数据','a')
            gotfile.write(result)
            gotfile.write('\n')
            gotfile.close()
        
if __name__ == '__main__':
    main()
