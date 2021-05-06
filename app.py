# !/usr/bin/python2
# coding:utf-8

import os
from dotenv import load_dotenv
from flask import *
import json
import pymysql
# from routes.attraction import getAttractions
import routes.attraction as attraction_api

load_dotenv()
os.environ

db_settings = {
    "host": os.environ["db_host"],    #主機
    "port": 3306,           #埠號    
    "user": os.environ["db_user"],         #使用者名稱
    "password": os.environ["db_password"], #使用者帳號
    "db": "tripWebsite",        #資料庫名稱
}

def db_connect():
    try:
        # 建立Connection物件
        connect = pymysql.connect(**db_settings)
        print("connect db_settings")
        return connect

    except Exception as ex:
        print(ex)
        return "資料庫連線失敗"

# 連線DB
cnnt=db_connect()

# 建立Cursor物件
cursor=cnnt.cursor()


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")



@app.route("/api/attractions", methods=["GET"])
def handleAttractions():
	page=request.args.get("page", 0)  #預設page值為0
	page=int(page)
	keyword=request.args.get("keyword", "")  #預設keyword值為""
	# print(page)
	# print(keyword)
	return attraction_api.getAttractions(page, keyword, cursor)
	


@app.route("/api/attraction/<attractionId>", methods=["GET"])
def handleAttraction(attractionId):
	# attractionId=int(attractionId)
	print(type(attractionId))
	return attraction_api.getAttraction(attractionId, cursor)


if (os.environ['localdebug']=='true'):
    app.run(port=3000)
else:
    app.run(port=3000, host='0.0.0.0')
	