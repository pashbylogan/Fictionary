from flask import Flask, Response, jsonify, request, redirect
from flask_cors import CORS
import pandas as pd
import json
import sys
from datetime import datetime
from termcolor import colored

sys.path.append('..')
import models.train as models

app = Flask(__name__)
cors = CORS(app)

MODEL_PATH = '../outputs/ud_full_2.19.22.bin'

API_KEYS = {
    'mHrzvi2MgYesVTNAeNM6Wk6UUQvJX3HWekiAqduoXIpIaPE1JyQj5Y4F2dqXsakLuXiHVFfVIr1ogAR32pyZsb4908X1K8A995NBSIv6sh8B0vABrs08O3otqdtL2KNb'
}

# ML model definition
loaded_models = {
    '1': 'data/dict-short.bin',
    '2': 'data/dict-long.bin',
    '3': 'data/urbandict.bin',
    '4': 'data/urbandict-long.bin',
}
# model = input(f"{loaded_models}\nEnter model number from above: ")
# weights = loaded_models[model]
model = models.get_model_for_api(weights_path=MODEL_PATH)

def authenticate_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("API-KEY")
        if api_key is None:
            return "API Key is missing", 401

        if api_key not in API_KEYS:
            return "Invalid API Key", 401

        return func(*args, **kwargs)

    return wrapper

@app.route('/word', methods=["POST"])
@authenticate_api_key
def word():
    data = request.json
    word = data['word']

    cols = 100

    # dd/mm/YY H:M:S
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(colored('\n' + '='*cols, 'cyan', attrs=['bold']), flush=True)
    print(dt_string, flush=True)

    try:
        definition = models.define(model, word, num_return=1)[0]
        definition = definition.replace(']', '').replace('[', '')\
                        .replace('fuck', 'duck').replace('cunt', 'trunk')\
                        .replace('sex', 'love').replace('genital', 'appendage')
        if definition[-1] != '.':
            definition += '.'
    except Exception as e:
        print(e)
        definition = "This word is undefinable. Good job..."

    print(colored('Prompt - ', 'magenta', attrs=['bold']) + word, flush=True)
    print(colored('Definition - ', 'magenta', attrs=['bold']) + definition, flush=True)
    print(colored('='*cols, 'cyan', attrs=['bold']), flush=True)

    resp_data = json.dumps(
            {'definition': definition}
        )
    response = Response(resp_data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = True
    return response  # return data with 200 OK

@app.route('/', methods=["GET"])
def index():
    return redirect(f'http://fictionary.loganpashby.com', 301)

if __name__ == '__main__':
    """
    # Load ML model
    for k, weights_path in loaded_models.items():
        loaded_models[k] = models.get_model(weights_path)
    """
    app.debug=False
    app.run(host='0.0.0.0', port=8000)  # run our Flask app
