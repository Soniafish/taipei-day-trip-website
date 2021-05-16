# !/usr/bin/python2
# coding:utf-8

import os
from dotenv import load_dotenv
from flask import *
import json
import pymysql
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

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

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
	# print(type(attractionId))
	return attraction_api.getAttraction(attractionId, cursor)


@app.route("/api/user", methods=["POST"]) #註冊
def handel_signup():
    try:
        insertValues=request.get_json()
        userName=insertValues["name"]
        userEmail=insertValues["email"]
        userPW=insertValues["password"]

        # 篩選資料表的資料
        result=cursor.execute("SELECT * FROM user where email='"+userEmail+"'")
        if result: # 註冊失敗:即資料表已有該使用者帳號
                return Response(
                        response=json.dumps({
                            "error": True,
                            "message": "註冊失敗，重複的Email或其他原因"
                        }),
                        status=200,
                        content_type='application/json'
                    )
            
        # 註冊成功：即資料表無該使用者帳號
        cursor.execute("INSERT INTO user(name, email, password)VALUES('" + userName + "','" + userEmail + "', '" + userPW + "')")
        cnnt.commit()
        return Response(
                        response=json.dumps({"ok": True}),
                        status=200,
                        content_type='application/json'
                    ) 
    except Exception as e:
        print(e) 
        return Response(
                    response=json.dumps({
                        "error": True,
                        "message": "系統錯誤"
                    }),
                    status=500,
                    content_type='application/json'
                )


@app.route("/api/user", methods=["PATCH"]) #登入
def handel_signin():
    try:
        insertValues=request.get_json()
        userEmail=insertValues["email"]
        userPW=insertValues["password"]
        # print("select * from user where email='"+userEmail+"' and password='"+userPW+"'")
        # 篩選資料表的資料
        result=cursor.execute("select * from user where email='"+userEmail+"' and password='"+userPW+"'")
        # print(result)
        if result:   # 登入成功：即帳號/密碼皆存在資料表
            select_data=cursor.fetchone()   #取得使用者資料
            session["userId"] = select_data[0]
            session["userName"] = select_data[1]
            session["userEmail"] = select_data[2]

            return Response(
                    response=json.dumps({"ok": True}),
                    status=200,
                    content_type='application/json'
                )
        
        # 登入失敗：即帳號或密碼不存在資料表
        return Response(
                    response=json.dumps({
                        "error": True,
                        "message": "帳號或密碼輸入錯誤"
                    }),
                    status=400,
                    content_type='application/json'
                )
    except Exception as e:
        print(e) 
        return Response(
                    response=json.dumps({
                        "error": True,
                        "message": "系統錯誤"
                    }),
                    status=500,
                    content_type='application/json'
                )


@app.route("/api/user", methods=["GET"]) #取得使用者資訊
def handel_userinfo():
    if "userId" in session:
        # print(session)
        return Response(
                    response=json.dumps({
                        "data": {
                            "id": session["userId"],
                            "name": session["userName"],
                            "email": session["userEmail"]
                        }
                    }),
                    status=200,
                    content_type='application/json'
                )
    else:
        return "null"
        

@app.route("/api/user", methods=["DELETE"]) #登出
def handel_signout():
    if "userId" in session:
        session.pop('userId', None)
        session.pop('userName', None)
        session.pop('userEmail', None)
        return Response(
                    response=json.dumps({"ok": True}),
                    status=200,
                    content_type='application/json'
                )
    else:
        return Response(
                    response=json.dumps({
                        "error": True,
                        "message": "系統錯誤"
                    }),
                    status=500,
                    content_type='application/json'
                )



if (os.environ['localdebug']=='true'):
    app.run(port=3000)
else:
    app.run(port=3000, host='0.0.0.0')
	