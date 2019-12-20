from flask import Flask, request
import requests
from decouple import config
import random
import bs4
import re

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world!'

api_url = 'https://api.telegram.org'
token = config('TOKEN')
chat_id = config('CHAT_ID')
naver_client_id = config('NAVER_CLIENT_ID')
naver_client_secret = config('NAVER_CLIENT_SECRET')

@app.route('/send/<text>')
def send(text):
    res = requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    return 'OK!'

@app.route('/chatbot', methods=['POST'])
def chatbot():
    from_telegram = request.get_json()
    chat_id = from_telegram.get('message').get('from').get('id')
    text = from_telegram.get('message').get('text')
    
    #메뉴 추천하기
    if text=='메뉴':
        menus = ['양자강','20층','김밥카페']
        lunch = random.choice(menus)
        response = lunch
    elif text=='메아':
        response = '응.'
    elif text=='이름':
        response = '메아 S 에페메랄.'
    elif text=='로또':
        lotto = random.sample(range(1,46),6)
        lotto = sorted(lotto)
        response = f'추천 로또 번호는{lotto}야'
    elif text[0:4]=='영번역 ':
        to_be_translate = text[4:]
        url='https://openapi.naver.com/v1/papago/n2mt'
        headers = {
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Naver-Client-Id':naver_client_id,
            'X-Naver-Client-Secret':naver_client_secret
        }
        data = f'source=ko&target=en&text={to_be_translate}'.encode('utf-8')
        res = requests.post(url,headers=headers,data=data).json()
        response = res.get('message').get('result').get('translatedText')
    elif text[0:4]=='일번역 ':
        to_be_translate = text[4:]
        url='https://openapi.naver.com/v1/papago/n2mt'
        headers = {
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Naver-Client-Id':naver_client_id,
            'X-Naver-Client-Secret':naver_client_secret
        }
        data = f'source=ko&target=ja&text={to_be_translate}'.encode('utf-8')
        res = requests.post(url,headers=headers,data=data).json()
        response = res.get('message').get('result').get('translatedText')    

    elif text=='날씨':
        html = requests.get('https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=09680101')

        soup = bs4.BeautifulSoup(html.text,'html.parser')
        weather = soup.select_one('#content > div.w_now2 > ul > li:nth-child(1) > div > em')
        weather = str(weather)
        weather = re.sub('<.+?>','',weather)
        weather = re.sub('&nbsp;| |\t|\r|\n','',weather)
        response = f'지금 서울 역삼동의 날씨는 {weather}야'
    else:
        response = f'{text} 가 무슨 말인지 모르겠어'



    res = requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={response}')
    
    #print(request.get_json())
    return 'ok',200
    # status code 200 -> ok! 잘 접수했다

# https://b0072674.ngrok.io

app.run(debug=True)