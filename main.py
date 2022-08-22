from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
yy_birthday = os.environ['YY_BIRTHDAY']
pp_birthday = os.environ['PP_BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  wea = weather['weather']
  wind = weather['wind']
  low_temp = math.floor(weather['low'])
  high_temp = math.floor(weather['high'])
  air = weather['airQuality']
  return wea, wind, low_temp, high_temp, air


def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days


def get_birthday(index):
  if index == 1:
    next = datetime.strptime(str(date.today().year) + "-" + yy_birthday, "%Y-%m-%d")
    if next < datetime.now():
      next = next.replace(year=next.year + 1)
    return (next - today).days
  if index == 2:
    next = datetime.strptime(str(date.today().year) + "-" + pp_birthday, "%Y-%m-%d")
    if next < datetime.now():
      next = next.replace(year=next.year + 1)
    return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, wind, low_temp, high_temp, air = get_weather()

data = {"weather":{"value": wea},
        "wind":{"value": wind},
        "air_Q":{"value": air},
        "low_temperature":{"value": low_temp},
        "high_temperature":{"value":high_temp},
        "love_days":{"value":get_count()},
        "yy_birthday_left":{"value":get_birthday(1)},
        "pp_birthday_left":{"value":get_birthday(2)},
        "words":{"value":get_words()}
        }

res = wm.send_template(user_id, template_id, data)
print(res)
