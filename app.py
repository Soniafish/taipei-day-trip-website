# !/usr/bin/python2
# coding:utf-8

import os
from dotenv import load_dotenv
from flask import *
import json
from mysql.connector import Error
from mysql.connector import pooling
import pymysql
import routes.attraction as attraction_api
import requests
import ssl      #mac才要加
ssl._create_default_https_context = ssl._create_unverified_context  #mac才要加
from datetime import datetime

# connection_pool = None
load_dotenv()
os.environ

# 建立connection_pool物件
connection_pool = pooling.MySQLConnectionPool(
    pool_name="pynative2_pool",
    pool_size=20,
    pool_reset_session=True,
    host=os.environ["db_host"],
    database='tripWebsite',
    user=os.environ["db_user"],
    password=os.environ["db_password"])
print("Printing connection pool properties ")
print("Connection Pool Name - ", connection_pool.pool_name)
print("Connection Pool Size - ", connection_pool.pool_size)

# 建立connection_pool物件for RDS
connection_pool2 = pooling.MySQLConnectionPool(
    pool_name="pynative2_pool2",
    pool_size=20,
    pool_reset_session=True,
    host=os.environ["db_host2"],
    database='web_tripalbum',
    user=os.environ["db_user2"],
    password=os.environ["db_password2"])
print("Printing connection pool properties ")
print("Connection Pool Name - ", connection_pool2.pool_name)
print("Connection Pool Size - ", connection_pool2.pool_size)

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
@app.route("/album")
def blogs():
    return render_template("album.html")


@app.route("/api/attractions", methods=["GET"])
def handleAttractions():
    # 建立cursor物件
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    print("connection_object_attractions")
    print(connection_object)
    print(cursor)

    #預設page值為0
    page=request.args.get("page", 0)
    page=int(page)
    keyword=request.args.get("keyword", "")  #預設keyword值為""
    # print(page)
    # print(keyword)

    # 關閉db連線
    result = attraction_api.getAttractions(page, keyword, cursor)
    cursor.close()
    connection_object.close()
    return result
    
@app.route("/api/attraction/<attractionId>", methods=["GET"])
def handleAttraction(attractionId):
    # 建立cursor物件
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()

    # attractionId=int(attractionId)
    # print(type(attractionId))

    # 關閉db連線
    result = attraction_api.getAttraction(attractionId, cursor)
    cursor.close()
    connection_object.close()
    return result


@app.route("/api/user", methods=["POST"]) #註冊
def handel_signup():
    # 建立cursor物件 
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()

    try:
        insertValues=request.get_json()
        userName=insertValues["name"]
        userEmail=insertValues["email"]
        userPW=insertValues["password"]

        # 篩選資料表的資料
        cursor.execute("SELECT * FROM user where email='"+userEmail+"'")
        filterData=cursor.fetchone()
        
        if filterData: # 註冊失敗:即資料表已有該使用者帳號
            cursor.close()
            connection_object.close()
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
        connection_object.commit()

        cursor.close()
        connection_object.close()
        return Response(
            response=json.dumps({"ok": True}),
            status=200,
            content_type='application/json'
        ) 
    except Exception as e:
        print(e) 
        cursor.close()
        connection_object.close()
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
    # 建立cursor物件 
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    print("connection_object_user")
    print(connection_object)
    print(cursor)
    
    try:
        insertValues=request.get_json()
        userEmail=insertValues["email"]
        userPW=insertValues["password"]
        
        # print("select * from user where email='"+userEmail+"' and password='"+userPW+"'")
        # 篩選資料表的資料
        cursor.execute("select * from user where email='"+userEmail+"' and password='"+userPW+"'")
        select_data=cursor.fetchone()#取得使用者資料
        # print(select_data)
        
        if select_data:   # 登入成功：即帳號/密碼皆存在資料表
        
            session["userId"] = select_data[0]
            session["userName"] = select_data[1]
            session["userEmail"] = select_data[2]

            cursor.close()
            connection_object.close()
            return Response(
                    response=json.dumps({"ok": True}),
                    status=200,
                    content_type='application/json'
                )
        
        # 登入失敗：即帳號或密碼不存在資料表
        cursor.close()
        connection_object.close()
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
        cursor.close()
        connection_object.close()
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


@app.route("/api/booking", methods=["GET"]) #取得未下單的預定行程
def handel_getBooking():
    # 建立cursor物件
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()

    if "userId" in session:
        userId = session["userId"]

        cursor.execute(f"select * from booking where userId='{userId}'")
        select_data=cursor.fetchone()
        print(select_data)

        if select_data:
            booking_attraction=select_data[2]
            booking_date=select_data[3]
            booking_time=select_data[4]
            booking_price=select_data[5]

            cursor.execute(f"select * from taipeiAttrations where id='{booking_attraction}'")
            select_data2=cursor.fetchone()
            attraction_name=select_data2[1]
            attraction_address=select_data2[4]
            attraction_imgs=select_data2[7].split(",")
            
            cursor.close()
            connection_object.close()
            return Response(
                response=json.dumps({
                    "data": {
                        "attraction": {
                        "id": booking_attraction,
                        "name": attraction_name,
                        "address": attraction_address,
                        "image": attraction_imgs[0]
                        },
                        "date": booking_date,
                        "time": booking_time,
                        "price": booking_price
                    }
                }),
                status=200,
                content_type='application/json'
            )

        cursor.close()
        connection_object.close()
        return Response(
            response=json.dumps({
                "data": None
            }),
            status=200,
            content_type='application/json'
        )

    cursor.close()
    connection_object.close()
    return Response(
        response=json.dumps({
            "error": True,
            "message": "未登入系統，拒絕存取"
        }),
        status=403,
        content_type='application/json'
    )        


@app.route("/api/booking", methods=["POST"]) #建立新的預定行程
def handel_setBooking():
    # 建立cursor物件 
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()

    if "userId" in session:
        try:
            userId = session["userId"]
            insertValues=request.get_json()
            attractionId=insertValues["attractionId"]
            date=insertValues["date"]
            time=insertValues["time"]
            price=insertValues["price"]

            if attractionId==None or date==None or time==None or price==None:
                return Response(
                    response=json.dumps({
                        "error": True,
                        "message": "建立失敗，輸入不正確或其他原因"
                    }),
                    status=400,
                    content_type='application/json'
                )

            # 篩選資料表的資料
            cursor.execute(f"SELECT * FROM booking where userId='{userId}'")
            filterData=cursor.fetchone()

            if filterData: # 使用者曾預定過行程:即資料表已有該使用者帳號
                print(f"UPDATE booking SET attractionId='{attractionId}', date='{date}', time='{time}', price='{price}' WHERE userId='{userId}'")
                cursor.execute(f"UPDATE booking SET attractionId='{attractionId}', date='{date}', time='{time}', price='{price}' WHERE userId='{userId}'")
            else: # 使用者未曾預定過行程:即資料表無該使用者帳號
                print(f"INSERT INTO booking(userId, attractionId, date, time, price)VALUES('{userId}','{attractionId}', '{date}', '{time}', '{price}')")
                cursor.execute(f"INSERT INTO booking(userId, attractionId, date, time, price)VALUES('{userId}','{attractionId}', '{date}', '{time}', '{price}')")
            connection_object.commit()
            cursor.close()
            connection_object.close()
            return Response(
                response=json.dumps({
                    "ok": True
                }),
                status=200,
                content_type='application/json'
            )

        except Exception as e:
            print(e) 
            cursor.close()
            connection_object.close()
            return Response(
                response=json.dumps({
                    "error": True,
                    "message": "伺服器內部錯誤"
                }),
                status=500,
                content_type='application/json'
            )

    cursor.close()
    connection_object.close()
    return Response(
        response=json.dumps({
            "error": True,
            "message": "未登入系統，拒絕存取"
        }),
        status=403,
        content_type='application/json'
    )
    

@app.route("/api/booking", methods=["DELETE"]) #刪除目前的預定行程
def handel_delBooking():
    # 建立cursor物件 
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()

    if "userId" in session:
        userId = session["userId"]
        cursor.execute(f"DELETE FROM booking WHERE userId='{userId}'")
        connection_object.commit()
        cursor.close()
        connection_object.close()
        return Response(
                response=json.dumps({
                    "ok": True
                }),
                status=200,
                content_type='application/json'
            )

    cursor.close()
    connection_object.close()
    return Response(
            response=json.dumps({
                "error": True,
                "message": "未登入系統，拒絕存取"
            }),
            status=403,
            content_type='application/json'
        )


@app.route("/api/orders", methods=["POST"]) #建立新訂單並完成付款
def handel_orders():
    # 建立cursor物件 
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()

    if "userId" in session:
        try:
            insertValues=request.get_json()
            # print(insertValues)
            prime=insertValues["prime"]
            price=insertValues["order"]["price"]
            attractionId=insertValues["order"]["trip"]["attraction"]["id"]
            attractionName=insertValues["order"]["trip"]["attraction"]["name"]
            attractionAddr=insertValues["order"]["trip"]["attraction"]["address"]
            attractionImg=insertValues["order"]["trip"]["attraction"]["image"]
            tripDate=insertValues["order"]["trip"]["date"]
            tripTime=insertValues["order"]["trip"]["time"]
            contactName=insertValues["order"]["contact"]["name"]
            contactPhone=insertValues["order"]["contact"]["phone"]
            contactEmail=insertValues["order"]["contact"]["email"]
            now = datetime.now()
            orderNumber=now.strftime("%Y%m%d%H%M%S")
            # print("date and time:"+orderNumber)
            userId=session["userId"]

            cursor.execute(f"INSERT INTO orders(number, userId, price, attractionId, attractionName, attractionAddr, attractionImg, tripDate, tripTime, contactName, contactEmail, contactPhone, status)VALUES('{orderNumber}','{userId}', '{price}', '{attractionId}', '{attractionName}', '{attractionAddr}', '{attractionImg}', '{tripDate}', '{tripTime}', '{contactName}', '{contactEmail}', '{contactPhone}', '{0}')")
            print("rowcount")
            print(cursor.rowcount)
            connection_object.commit()

            if cursor.rowcount: #訂單成立           
                url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
                headers = {
                    "Content-Type":"application/json",
                    "x-api-key": os.environ["partner_key"],
                }
                payload = json.dumps({
                    "prime": prime,
                    "partner_key": os.environ["partner_key"],
                    "merchant_id": os.environ["merchant_id"],
                    "details": "TapPay Test",
                    "amount": price,
                    "cardholder": {
                        "phone_number": contactPhone,
                        "name": contactName,
                        "email": contactEmail
                    },
                    "remember": True
                })
                # print("payload:"+payload)
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)

                handel_delBooking()

                if json.loads(response.text)["status"] == 0:
                    cursor.execute(f"UPDATE orders SET status='{1}' WHERE number='{orderNumber}'")
                    connection_object.commit()
                    cursor.close()
                    connection_object.close()
                    return Response(
                        response=json.dumps({
                            "data": {
                                "number": "20210425121135",
                                "payment": {
                                    "status": 0,
                                    "message": "付款成功"
                                }
                            }
                        }),
                        status=200,
                        content_type='application/json'
                    )

                cursor.close()
                connection_object.close()
                return Response(
                    response=json.dumps({
                        "data": {
                            "number": "20210425121135",
                            "payment": {
                                "status": 0,
                                "message": "付款失敗"
                            }
                        }
                    }),
                    status=200,
                    content_type='application/json'
                )

            cursor.close()
            connection_object.close()
            return Response(
                response=json.dumps({
                    "error": True,
                    "message": "訂單建立失敗"
                }),
                status=400,
                content_type='application/json'
            ) 

        except Exception as e:
            print(e) 
            cursor.close()
            connection_object.close()
            return Response(
                response=json.dumps({
                    "error": True,
                    "message": "系統錯誤"
                }),
                status=500,
                content_type='application/json'
            )
    else:
        cursor.close()
        connection_object.close()
        return Response(
                response=json.dumps({
                    "error": True,
                    "message": "未登入系統"
                }),
                status=403,
                content_type='application/json'
            )

@app.route("/api/album", methods=["GET"]) #取得相簿資料
def handel_getAlbum():
    # 建立cursor物件
    connection_object2 = connection_pool2.get_connection()
    cursor = connection_object2.cursor()

    cursor.execute(f"SELECT * FROM web_tripalbum ORDER BU id DESC")
    filterData=cursor.fetchall() #取得album圖片資料
    print(filterData[0])

    if filterData:
        data=[]
        for item in filterData:
            data.append({
                "title": item[1],
                "img": item[3],
                "date": item[4]
            })

        cursor.close()
        connection_object2.close()
        return Response(
            response=json.dumps({
                "data": data
                }),
            status=200,
            content_type='application/json'
        )

    cursor.close()
    connection_object2.close()
    return Response(
        response=json.dumps({
            "error": true,
            "message": "系統錯誤"
            }),
        status=500,
        content_type='application/json'
    )  


@app.route("/api/album", methods=["POST"]) #建立相簿照片(
def handel_setAlbum():
    # 建立cursor物件 
    connection_object2 = connection_pool2.get_connection()
    cursor = connection_object2.cursor()

    if "userId" in session:
        try: 
            insertValues=request.get_json()
            print(insertValues)
            userId=session["userId"]
            album_title=insertValues["title"]
            album_date=insertValues["date"]
            album_imgurl=insertValues["url"]
            if userId==None or album_title==None or album_date==None or album_imgurl==None:
                return Response(
                    response=json.dumps({
                        "error": True,
                        "message": "相簿檔案建立失敗，輸入不正確或其他原因"
                    }),
                    status=400,
                    content_type='application/json'
                )

            # 篩選資料表的資料
            cursor.execute(f"SELECT * FROM web_tripalbum WHERE img='{album_imgurl}'")
            filterData=cursor.fetchone()

            if filterData: # 使用者曾預定過行程:即資料表已有該使用者帳號
                print(f"UPDATE web_tripalbum SET title='{album_title}', userid='{userId}', date='{album_date}' WHERE img='{album_imgurl}'")
                cursor.execute(f"UPDATE web_tripalbum SET title='{album_title}', userid='{userId}', date='{album_date}' WHERE img='{album_imgurl}'")
            else: # 使用者未曾預定過行程:即資料表無該使用者帳號
                print(f"INSERT INTO web_tripalbum(title, userid, img, date)VALUES('{album_title}','{userId}', '{album_imgurl}', '{album_date}')")
                cursor.execute(f"INSERT INTO web_tripalbum(title, userid, img, date)VALUES('{album_title}','{userId}', '{album_imgurl}', '{album_date}')")
            connection_object2.commit()
            cursor.close()
            connection_object2.close()
            return Response(
                response=json.dumps({
                    "ok": True
                }),
                status=200,
                content_type='application/json'
            )

        except Exception as e:
            print(request.get_json()) 
            print(e) 
            cursor.close()
            connection_object2.close()
            return Response(
                response=json.dumps({
                    "error": True,
                    "message": "伺服器內部錯誤"
                }),
                status=500,
                content_type='application/json'
            )

    cursor.close()
    connection_object2.close()
    return Response(
        response=json.dumps({
            "error": True,
            "message": "未登入系統，拒絕存取"
        }),
        status=403,
        content_type='application/json'
    )



if (os.environ['localdebug']=='true'):
    app.run(port=3000)
else:
    app.run(port=3000, host='0.0.0.0')
    