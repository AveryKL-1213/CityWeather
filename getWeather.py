import re
import json
import requests
from bs4 import BeautifulSoup


class SearchWeather():
    def __init__(self):
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ''(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    def getcityCode(self, cityName):
        try:
            jsonWeather = open(r"CityWeather/citycode.json",
                               'r', encoding='utf-8')
            jsonread = json.load(jsonWeather)
            sname = cityName
            scode = ""
            for s in jsonread:
                if(sname == s["city_name"]):
                    scode = s["city_code"]
            return scode
        except Exception as e:
            print(repr(e))

    def getWeather(self, cityCode, cityname):
        url = 'http://www.weather.com.cn/weather/%s.shtml' % cityCode
        html = requests.get(url, headers=self.HEADERS)
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'lxml')
        weather = "日期      天气    【温度】    风向风力\n"
        for item in soup.find("div", {'id': '7d'}).find('ul').find_all('li'):
            date, detail = item.find('h1').string, item.find_all('p')
            title = detail[0].string
            templow = detail[1].find("i").string
            temphigh = detail[1].find(
                'span').string if detail[1].find('span') else ''
            wind, direction = detail[2].find(
                'span')['title'], detail[2].find('i').string
            if temphigh == '':
                weather += '你好，【%s】今天白天：【%s】，温度：【%s】，%s：【%s】\n' % (
                    cityname, title, templow, wind, direction)
            else:
                weather += (date + title + "【" + templow + "~" +
                            temphigh + '°C】' + wind + direction + "\n")
        return weather

    def main(self, city):
        cityCode = self.getcityCode(city)
        detail = self.getWeather(cityCode, city)
        print(detail)


if __name__ == "__main__":
    weather = SearchWeather()
    weather.main(city=input('请输入城市名称：'))