import re
import json
import requests
from bs4 import BeautifulSoup
from time import sleep
import urllib


class CityWeather():
    def __init__(self):
        self.HEADERS = {  # 设置UA
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ''(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    def getcityCode(self, cityName):  # 获取城市对应的邮编
        try:
            count = 0
            while(True):
                jsonCityCode = open(r"CityWeather/citycode.json",
                                    'r', encoding='utf-8')
                jsonread = json.load(jsonCityCode)
                cname = cityName
                ccode = ""
                for s in jsonread:
                    if(cname == s["city_name"]):
                        ccode = s["city_code"]
                if ccode == "":  # 确认得到城市的邮编，否则要求用户重新输入
                    cityName = input("请输入正确的城市名(非省级)：")
                else:
                    return ccode
                count += 1
                if count > 3:  # 输入错误达上限，退出程序
                    print("连续输入错误城市名5次，系统关闭...")
                    sleep(3)
                    exit(0)
        except Exception as e:
            print(repr(e))

    def getWeather(self, cityCode, cityname):  # 爬取中国天气网对应城市的天气信息
        url = 'http://www.weather.com.cn/weather/%s.shtml' % cityCode
        html = requests.get(url, headers=self.HEADERS)
        html.encoding = 'utf-8'
        bSoup = BeautifulSoup(html.text, 'lxml')
        weather = "日期      天气    【温度】    风向风力\n"
        for item in bSoup.find("div", {'id': '7d'}).find('ul').find_all('li'):
            date, detail = item.find('h1').string, item.find_all('p')
            title = detail[0].string
            templow = detail[1].find("i").string
            if detail[1].find('span'):
                temphigh = detail[1].find('span').string
            else:
                temphigh = ''
            wind, direction = detail[2].find(
                'span')['title'], detail[2].find('i').string
            if temphigh == '':
                weather += '你好，【%s】今天白天：【%s】，温度：【%s】，%s：【%s】\n' % (
                    cityname, title, templow, wind, direction)
            else:
                weather += (date + title + "【" + templow + "-" +
                            temphigh + '°C】' + wind + direction + "\n")
        return weather

    def main(self, city):
        cityCode = self.getcityCode(city)
        detail = self.getWeather(cityCode, city)
        print(detail)


if __name__ == "__main__":
    weather = CityWeather()
    weather.main(city=input('请输入城市名称：'))
