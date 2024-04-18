import requests

def func():
    r = requests.get('https://newsapi.org/v2/everything?qInTitle=stock%20market&from=2023-7-16&to=2023-7-17&sortBy=popularity&language=en&apiKey=890603a55bfa47048e4490069ebee18c')
    result = r.json()
    result = result['articles']
    result

# def func():
#     import requests
#     r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q=Aleppo&APIID=26631f0f41b95fb9f5ac0df9a8f43c92&units=metric')
#     result = r.json()
#     result


def fun2():
    url = 'https://api.languagetool.org/v2/check'
    data = {
        'text': 'This is an nice day',
        'language': 'en-US'
    }
    response = requests.post(url, data=data)
    result = response.json()
    result


# if __name__ == '__main__':
    # func()


from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Currency Rate API</h1> <a href=http://127.0.0.1:5000/api/v1/rr/?from=USD&to=AUD>link text</a> "

@app.route('/api/v1/rr/')
def get_conversion_rate():
    from_c = request.args.get('from', None, str)
    to_c = request.args.get('to', None, str)
    print(from_c, to_c)
    return "123"

app.run(host='0.0.0.0')
