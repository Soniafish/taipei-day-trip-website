# !/usr/bin/python2
# coding:utf-8

import os
from dotenv import load_dotenv
from flask import *
import json
import pymysql

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
def getAttractions():

	# content_type = request.headers['Content-Type']
    # if content_type != 'application/json':
	# 	return json.dumps({"error":"bad request"})

	# else:

		page=request.args.get("page", 0)  #預設page值為0
		page=int(page)
		keyword=request.args.get("keyword", "")  #預設keyword值為""
		# print(page)
		# print(keyword)
		statement=""
		p_min = 12 * page
		p_max = 12 * (page + 1) - 1 
		if keyword=="":
			statement=f"select id, name, category, description, address, transport, mrt, latitude, longitude, images from taipeiAttrations order by id limit {p_min},{p_min}"
		else:
			statement ="select id, name, category, description, address, transport, mrt, latitude, longitude, images from taipeiAttrations where category like '%"+keyword+f"%' order by id limit {p_min},{p_max}"
		# print(statement)
		
		result=cursor.execute(statement)
		# print(result)
		if result:   
			filterData=cursor.fetchall()   #取得景點

			# print(filterData)
			data=[]
			for item in filterData:
				images=item[9].split(",")
				data.append({
					"id": item[0],
					"name": item[1],
					"category": item[2],
					"description": item[3],
					"address": item[4],
					"transport": item[5],
					"mrt": item[6],
					"latitude": item[7],
					"longitude": item[8],
					"images": images[0: -1]
				})
			return json.dumps({
					"nextPage": page+1,
					"data": data
					})

		else:
			return json.dumps({
					"nextPage": 0,
					"data": ''
					})
			
		return json.dumps({
				"error": true,
				"message": "系統錯誤"
				})


@app.route("/api/attraction/<attractionId>", methods=["GET"])
def getAttraction(attractionId):

	# content_type = request.headers['Content-Type']
    # if content_type != 'application/json':
	# 	return json.dumps({"error":"bad request"})

	# else:
		statement=f"select id, name, category, description, address, transport, mrt, latitude, longitude, images from taipeiAttrations where id={attractionId}"
		result=cursor.execute(statement)
		if result:
			filterData=cursor.fetchone()
			# print(filterData)
			images=filterData[9].split(",")
			data={
				"id": filterData[0],
				"name": filterData[1],
				"category": filterData[2],
				"description": filterData[3],
				"address": filterData[4],
				"transport": filterData[5],
				"mrt": filterData[6],
				"latitude": filterData[7],
				"longitude": filterData[8],
				"images": images[0: -1]
			}
			return json.dumps({"data": data})

		else:
			return json.dumps({
						"error": true,
						"message": "景點編號不正確"
					})

		return json.dumps({
					"error": true,
					"message": "自訂的錯誤訊息"
				})


if (os.environ['localdebug']=='true'):
    app.run(port=3000)
else:
    app.run(port=3000, host='0.0.0.0')