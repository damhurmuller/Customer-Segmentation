import os
import pandas as pd
import requests
from flask import Flask, request, Response

dataset_path = 'rfm.csv'
TOKEN = '1312157400:AAF9-_4si7P8gcxbzZMY3vGnAKR4qOsDDqM'

def send_message(chat_id, text):
    url = 'https://api.telegram.org/bot{}/'.format(TOKEN)
    url = url + 'sendMessage?chat_id={}'.format(chat_id)

    r = requests.post(url, json={"text": text})
    print('Status Code {}'.format(r.status_code))

    return None

def load_dataset(path):
    df  = pd.read_csv(path)

    return df

def get_user(data):
    rfm = load_dataset(dataset_path)

    if data in rfm['customer_id'].values:
        data = data
        url = 'https://retail-rfm-segmentation.herokuapp.com/customers/{}'.format(data)
        r = requests.get(url)

        print('Status Code {}'.format(r.status_code))

        df = pd.DataFrame([r.json()])

        return df
    else:
        return 'error'

def parse_message(message):
    chat_id = message["message"]["chat"]["id"]
    customer_id = message["message"]["text"]

    customer_id = customer_id.replace('/','')

    try:
        customer_id = int(customer_id)

    except ValueError:
        customer_id = 'error'

    return chat_id, customer_id

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.get_json()

        chat_id, customer_id = parse_message(message)

        if customer_id != 'error':
            df = get_user(customer_id)

            if isinstance(df, pd.DataFrame):
                msg = 'Customer ID {} belongs to Segment {}'.format(
                        df['customer_id'].values[0],
                        df['segment'].values[0])

                send_message(chat_id, msg)
                return Response('Ok', status=200)
            else:
                send_message(chat_id, 'Customer ID Not Avaiable')
                return Response('Ok', status=200)
        else:
            send_message(chat_id, 'Customer ID is Wrong')
            return Response('Ok', status=200)
    else:
        return '<h1> Customer Segmentation BOT </h1>'

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port, debug=True)
