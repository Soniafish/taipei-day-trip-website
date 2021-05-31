# !/usr/bin/python2
# coding:utf-8

import os
from dotenv import load_dotenv
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
cursor.execute("use tripWebsite")

# number, userId, price, attractionId, attractionName, attractionAddr, attractionImg, tripDate, tripTime, contactName, contactEmail, contactPhone, status (tinyint / 0 表示 false, 1 表示 true)
cursor.execute("create table orders(number varchar(255) primary key, userId bigint not null, price mediumint not null, attractionId varchar(255) not null, attractionName varchar(255) not null, attractionAddr varchar(255) not null, attractionImg text not null, tripDate  varchar(255) not null, tripTime tinytext not null, contactName varchar(255) not null, contactEmail varchar(255) not null, contactPhone tinytext not null, status tinyint not null)")
cnnt.commit()