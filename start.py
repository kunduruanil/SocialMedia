"""
@author  Anil Kumar Reddy Kunduru
@Date 3nd oct 2020
"""

from flask import Flask,request,jsonify
from app_route.all_apis import *
import ast
from bson import json_util

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)


# The route() function of the Flask class is a decorator,
@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/login', methods = ['POST'])
def login_user():
    try:
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
            else:
                data = request.data
                data = ast.literal_eval(data.decode("UTF-8"))
            id = create_user(data=data)
            return jsonify({"code":200,"value":id})
        else:
            return jsonify({"code":400,"msg":"Bad request"})
    except Exception as e:
        print(str(e))
        return jsonify({"code":500,"msg":"Internal Server Error"})


@app.route('/createconfig', methods = ['POST'])
def create_user_config():
    try:
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
            else:
                data = request.data
                data = ast.literal_eval(data.decode("UTF-8"))
            id = create_config(data=data)
            return jsonify({"code":200,"value":id})
        else:
            return jsonify({"code":400,"msg":"Bad request"})
    except Exception as e:
        print(str(e))
        return jsonify({"code":500,"msg":"Internal Server Error"})

@app.route('/updateconfig', methods = ['POST'])
def update_user_config():
    try:
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
            else:
                data = request.data
                data = ast.literal_eval(data.decode("UTF-8"))
            id = update_config(data=data)
            return jsonify({"code":200,"value":id})
        else:
            return jsonify({"code":400,"msg":"Bad request"})
    except Exception as e:
        print(str(e))
        return jsonify({"code":500,"msg":"Internal Server Error"})


@app.route('/listcofigs', methods = ['POST'])
def list_all_cofigs():
    try:
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
            else:
                data = request.data
                data = ast.literal_eval(data.decode("UTF-8"))
            list_all = get_all_cofig_by_userid(query=data)
            # print(list_all)
            return jsonify(json_util.dumps({"code":200,"value":list_all}))
        else:
            return jsonify({"code":400,"msg":"Bad request"})
    except Exception as e:
        print(str(e))
        return jsonify({"code":500,"msg":"Internal Server Error"})

@app.route('/checklogin', methods = ['POST'])
def user_validation():
    try:
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
            else:
                data = request.data
                data = ast.literal_eval(data.decode("UTF-8"))
            user = check_user_login(query=data)
            return jsonify(json_util.dumps({"code":200,"value":user}))
        else:
            return jsonify({"code":400,"msg":"Bad request"})
    except Exception as e:
        print(str(e))
        return jsonify({"code":500,"msg":"Internal Server Error"})


@app.route('/getrecordcountskw', methods = ['POST'])
def record_count_search_keyword():
    try:
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
            else:
                data = request.data
                data = ast.literal_eval(data.decode("UTF-8"))
            count = get_search_keyword_count(query=data)
            return jsonify(json_util.dumps({"code":200,"value":count}))
        else:
            return jsonify({"code":400,"msg":"Bad request"})
    except Exception as e:
        print(str(e))
        return jsonify({"code":500,"msg":"Internal Server Error"})

@app.route('/getcountsofgroupsskw', methods = ['POST'])
def counts_of_groups_search_keyword():
    try:
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
            else:
                data = request.data
                data = ast.literal_eval(data.decode("UTF-8"))
            stats = get_counts_of_groups_search_keyword(query=data)
            return jsonify(json_util.dumps({"code":200,"value":stats}))
        else:
            return jsonify({"code":400,"msg":"Bad request"})
    except Exception as e:
        print(str(e))
        return jsonify({"code":500,"msg":"Internal Server Error"})

# main driver function
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,  debug=True)