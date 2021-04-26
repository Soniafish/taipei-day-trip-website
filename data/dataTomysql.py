# !/usr/bin/python2
# coding:utf-8

import os
from dotenv import load_dotenv
import json
import pymysql

load_dotenv()
os.environ

db_settings = {
    "host": os.environ["db_host"],    #主機
    "port": 3306,           #埠號    
    "user": os.environ["db_user"],         #使用者名稱
    "password": os.environ["db_password"], #使用者帳號
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

# cursor.execute("create database tripWebsite")
cursor.execute("use tripWebsite")
cursor.execute("create table taipeiAttrations(id bigint PRIMARY KEY, name VARCHAR(255) NOT NULL, category VARCHAR(255) NOT NULL, description TEXT NOT NULL, address VARCHAR(255) NOT NULL, mrt VARCHAR(255), transport TEXT, images TEXT NOT NULL, latitude FLOAT, longitude FLOAT, postDate datetime NOT NULL)")


data=None
with open("taipei-attractions.json", mode="r") as file:
    data=json.load(file)
    data=data["result"]["results"]

valList=[]
for item in data:
    _id=item["_id"]   #編號
    name=item["stitle"] #景點名
    # cat1=item["CAT1"] #類型:景點
    category=item["CAT2"] #類型:溫泉區
    description=item["xbody"]   #說明
    address=item["address"]   #地址
    mrt=item["MRT"]   #捷運站
    transport=item["info"] #搭車資訊
    # imgs=item["file"] #圖檔路徑
    imgs=item["file"].split("http://")
    newImgs=""
    for idx in range(1, len(imgs)):
        if imgs[idx][-4:].lower() == ".jpg" or imgs[idx][-4:].lower() == ".png":
            newImgs=newImgs+"http://"+imgs[idx]+","

    # print(newImgs)
    postDate=item["xpostDate"]  #po文日期
    latitude=item["latitude"]    #緯度
    longitude=item["longitude"]  #經度
    
    val = (_id, name, category, description, address, mrt, transport, newImgs, postDate, latitude, longitude)
    valList.append(val)
    # print(val)
    
sql = "INSERT INTO taipeiAttrations (id, name, category, description, address, mrt, transport, images, postDate, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
cursor.executemany(sql, valList)
    
cnnt.commit()    

