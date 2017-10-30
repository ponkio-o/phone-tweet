#coding:utf-8
from requests_oauthlib import OAuth1Session
import json
import settings
import requests
import urllib
 
#APIからトークンの取得
def authorize():
 
    url = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"
 
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Ocp-Apim-Subscription-Key": settings.SPEECH_API_KEY
    }
 
    response = requests.post(url, headers=headers)
 
    if response.ok:
        _body = response.text
        return _body
    else:
        response.raise_for_status()

#取得したトークンを格納する
token = authorize()

#ファイルの選択
infile = open("record.wav","r")
data = infile.read()


#APIに投げて結果をもらう
def speech_to_text( raw_data, token, lang="ja-JP", samplerate=8000, scenarios="ulm"):
    data = raw_data
    params = {
        "version": "3.0",
        "requestid": "b2c95ede-97eb-4c88-81e4-80f32d6aee54",
        "appid": "D4D52672-91D7-4C74-8AD8-42B1D98141A5",
        "format": "json",
        "locale": lang,
        "device.os": "Windows",
        "scenarios": scenarios,
        "instanceid": "565D69FF-E928-4B7E-87DA-9A750B96D9E3" 
    }
     
    url = "https://speech.platform.bing.com/recognize?" + urllib.urlencode(params)
    headers = {"Content-type": "audio/wav; samplerate={0}".format(samplerate),
               "Authorization": "Bearer " + token }
     
    response = requests.post(url, data=data, headers=headers)
     
    if response.ok:
        result = response.json()["results"][0]
        return result["lexical"]
    else:
        raise response.raise_for_status()

#APIで取得したデータを格納する
message = speech_to_text(data,token,lang="ja-JP", samplerate=8000, scenarios="ulm")


#settings.pyからTokenを取得
twitter = OAuth1Session(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

#ツイート
params = {"status":"%s"%message}
req = twitter.post("https://api.twitter.com/1.1/statuses/update.json",params = params)
