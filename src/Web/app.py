from flask import Flask, render_template, jsonify, request,redirect,url_for
from web_config import web_host, web_port
import os
import json
from dataset import tolist,combine,covid_list,income_list,sentiment_list,map_col

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

@app.route('/display',methods=['POST'])
def display():
    try:
        #data from web interface - Scenario Selector and Graph Type Option Box
        data=request.json
    except Exception as e:
        print(e)
    result={}
    if data['sel_case']=="Covid VS Income":
        combine_data=combine(income_list,covid_list)
        result['data']=combine_data
        result['xlabel']='Mean income per person (AUD)'
        result['ylabel']='Average number of tweets related to covid19 per person'
        result['title']=data['sel_case']
    elif data['sel_case']=="Sentiment VS Income":
        combine_data=combine(income_list,sentiment_list)
        result['data'] = combine_data
        result['xlabel'] = 'Mean income per person (AUD)'
        result['ylabel'] = 'Average sentiment score'
        result['title'] = data['sel_case']
    elif data['sel_case']=="Sentiment VS Covid":
        combine_data=combine(covid_list,sentiment_list)
        result['data'] = combine_data
        result['xlabel'] = 'Average number of tweets related to covid19 per person'
        result['ylabel'] = 'Average sentiment score'
        result['title'] = data['sel_case']
    print(result)
    return jsonify(result)


@app.route('/map',methods=['POST','PUT','GET'])
def map():
    # bar()
    try:
        data = request.json
    except Exception as e:
        print(e)
    result=map_col
    print(result)
    return jsonify(result)

# @app.route('/map_covid',methods=['GET'])
# def bar():
#     return render_template("map_covid.html")


if __name__ == '__main__':
    app.debug=True
    app.run(host=web_host,port=web_port)