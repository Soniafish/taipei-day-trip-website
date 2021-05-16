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
cursor.execute("create table user(id bigint primary key auto_increment, name varchar(255) not null, email varchar(255) not null, password varchar(255) not null, time datetime not null default current_timestamp)")
cursor.execute("INSERT INTO user (name, email, password) VALUES ('admin','admin@gmail.com', 'admin1234')")
cnnt.commit()