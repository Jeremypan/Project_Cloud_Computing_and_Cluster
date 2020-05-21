from flask import Flask, render_template, jsonify, request
import os
import json

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')

app = Flask(__name__, instance_relative_config=True)


with open(os.path.join(APP_STATIC, 'home_page_options.json')) as file:
    options_json = json.load(file)
    option_list = options_json["option_list"]

@app.route('/')
def home():
    """
    home page
    :return: html template
    """
    return render_template("home.html",option_list=option_list)

@app.route('/display')
def display():
    try:
        data=request.json
    except Exception as e:
        print(e)
    return str(data)

if __name__ == '__main__':
    # app.debug=True
    app.run()