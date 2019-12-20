from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world!'

api_url = 'https://api.telegram.org'
token = '1008408942:AAE49DpolKuuVbJxkP5F-SAUWo_mA9m9vW0'
chat_id = '958067137'

@app.route('/send/<text>')
def send(text):
    res = requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    return 'OK!'



# 토큰 1008408942:AAE49DpolKuuVbJxkP5F-SAUWo_mA9m9vW0
# https://api.telegram.org/bot<token>/METHOD_NAME
# ID: 958067137

app.run(debug=True)