import requests
import json
from bs4 import BeautifulSoup
from time import sleep


class CityWeather():
    def __init__(self):
        self.cityName = ""  # 城市名
        self.HEADERS = {  # 设置UA
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15'}

    def getCityCode(self):  # 获取城市对应的邮编
        try:
            count = 0
            while(True):
                jsonCityCode = open(r"CityWeather/citycode.json",
                                    'r', encoding='utf-8')
                jsonread = json.load(jsonCityCode)
                cname = self.cityName
                ccode = ""
                for s in jsonread:
                    if(cname == s["city_name"]):
                        ccode = s["city_code"]
                if ccode == "":  # 确认得到城市的邮编，否则要求用户重新输入
                    self.cityName = input("请输入正确的城市名(非省级)：")
                else:
                    return ccode
                count += 1
                if count > 3:  # 输入错误达上限，退出程序
                    print("连续输入错误城市名5次，系统关闭...")
                    sleep(3)
                    exit(0)
        except Exception as e:
            print(repr(e))

    def getWeather(self, cityCode):  # 爬取中国天气网对应城市的天气信息
        url = 'http://www.weather.com.cn/weather/%s.shtml' % cityCode
        html = requests.get(url, headers=self.HEADERS)
        html.encoding = 'utf-8'
        bSoup = BeautifulSoup(html.text, 'lxml')
        day = 0
        # 爬取
        for item in bSoup.find("div", {'id': '7d'}).find('ul').find_all('li'):
            date, WeatherInfo = item.find('h1').string, item.find_all('p')
            title = WeatherInfo[0].string
            low_temp = WeatherInfo[1].find("i").string
            if WeatherInfo[1].find('span'):
                high_temp = WeatherInfo[1].find('span').string
            else:  # 网页会出现当天没有最高温的情况
                high_temp = ''
            wind, direction = WeatherInfo[2].find(
                'span')['title'], WeatherInfo[2].find('i').string
            if high_temp == '' and day == 0:  # 网页会出现当日天气没有最高温的情况
                weather = '\n%s \n今日天气：%s\n温度：%s\n风力：%s%s\n' % (
                    self.cityName, title, low_temp, wind, direction) + "\n七日内天气预报：\n日期\t\t天气\t\t\t温度\t\t\t风力\n"
            elif day == 0:
                weather = '\n%s \n今日天气：%s\n温度：%s  ~ %s\n%s风力：%s\n' % (
                    self.cityName, title, low_temp, high_temp + low_temp[-1], wind, direction) + "\n七日内天气预报：\n日期\t\t天气\t\t\t温度\t\t\t风力\n"
            else:
                weather += (date + "\t" + "%.5s" % title + "\t\t" + low_temp + "  ~ " +
                            high_temp + low_temp[-1] + "\t\t\t" + wind + direction + "\n")
            day += 1
        return weather

    def main(self, city):
        self.cityName = city
        cityCode = self.getCityCode()
        detail = self.getWeather(cityCode)
        print(detail)


if __name__ == "__main__":
    weather = CityWeather()
    city = input('请输入城市名称：')
    weather.main(city)
