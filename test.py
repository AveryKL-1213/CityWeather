import json
import requests

jsonWeather = open(r"CityWeather/citycode.json", 'r', encoding='utf-8')
jsonread = json.load(jsonWeather)

sname = input("City: ")
scode = ""
for s in jsonread:
    if(sname == s["city_name"]):
        scode = s["city_code"]

if(scode == ""):
    print("XXXXX")
    exit(0)

url = r"http://t.weather.itboy.net/api/weather/city/"+scode
response = requests.get(url)
response.raise_for_status()
weatherData = json.loads(response.text)
w = weatherData["data"]
print(w)
print(w["wendu"])
print("明日最"+w["forecast"][0]["high"])
print("明日最"+w["forecast"][0]["low"])
print("明日天气："+w["forecast"][0]["type"])
