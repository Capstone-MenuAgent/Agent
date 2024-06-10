from datetime import datetime
from dotenv import load_dotenv
import json
import os
import requests
import pandas as pd

load_dotenv()
WEATHER_KEY = os.getenv("WEATHER_KEY")

def getNowDate():
    now = datetime.now()
    date = now.strftime('%Y%m%d')
    hour = now.hour - (1 if now.minute < 45 else 0)
    time = "%02d30" % hour
    return {'date': date, 'time': time}

def skyCode(code):
    code = int(code)
    if code <= 5:
        return '맑음'
    elif code <= 8:
        return '구름많음'
    else:
        return '흐림'

def getWeatherFore():
    apiURL = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    date = getNowDate()
    base_date = date['date']
    base_time = date['time']
    key = WEATHER_KEY
    params = {
        'serviceKey': key,
        'pageNo': 1,
        'numOfRows': 1000,
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': '76',
        'ny': '114'
    }
    response = requests.get(apiURL, params=params)
    if response.status_code == 200:
        weatherJSON = response.json()
        weatherJSON = weatherJSON['response']['body']['items']['item']
    else:
        return 'error'

    df = pd.DataFrame(weatherJSON)
    weather = {}
    for i in range(len(df)):
        p = df.loc[i]
        time, cat, value = p['fcstTime'], p['category'], p['fcstValue']
        if not weather.get(time):
            weather[time] = {}
        if cat == 'T1H':
            weather[time].update({'기온': value})
        elif cat == 'SKY':
            weather[time].update({'하늘': skyCode(value)})

    return weather