# !/usr/bin/python2
# coding:utf-8
from flask import *
import json
import pymysql

def getAttractions(page, keyword, cursor):   
	# print(page , keyword)
	statement=""
	p_idx = 12 * page
	p_count = 12
	nextPage = page+1
	
	if keyword=="":
		cursor.execute("select count(*) from taipeiAttrations")
		count=cursor.fetchone()
		# print("count")
		# print(count[0])
		if count[0] < p_idx:
			return Response(
				response=json.dumps({
					"nextPage": None,
					"data": []
					}),
				status=200,
				content_type='application/json'
			)
		elif count[0] <  12 * (page + 1):
			p_count = count[0] % 12
			nextPage = None
			# print("p_count:", p_count)
		statement=f"select id, name, category, description, address, transport, mrt, latitude, longitude, images from taipeiAttrations order by id limit {p_idx},{p_count}"
	else:
		cursor.execute("select count(*) from taipeiAttrations where name like '%"+keyword+"%'")
		count=cursor.fetchone()
		# print(count[0])
		if count[0] <  12 * (page + 1):
			p_count = count[0] % 12
			nextPage = None
			# print("p_count:", p_count)
		statement ="select id, name, category, description, address, transport, mrt, latitude, longitude, images from taipeiAttrations where name like '%"+keyword+f"%' order by id limit {p_idx},{p_count}"
	# print(statement)
	
	cursor.execute(statement)
	filterData=cursor.fetchall() #取得景點
	# print("filterData")
	# print(filterData)

	if filterData:   
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

			# print(data[0]["images"])

		return Response(
				response=json.dumps({
					"nextPage": nextPage,
					"data": data
					}),
				status=200,
				content_type='application/json'
			)

	else:
		return Response(
				response=json.dumps({
					"nextPage": None,
					"data": []
					}),
				status=200,
				content_type='application/json'
			)
	
	
	return Response(
				response=json.dumps({
					"error": true,
					"message": "系統錯誤"
					}),
				status=500,
				content_type='application/json'
			)


def getAttraction(attractionId, cursor):
	statement=f"select id, name, category, description, address, transport, mrt, latitude, longitude, images from taipeiAttrations where id={attractionId}"
	cursor.execute(statement)
	filterData=cursor.fetchone()
	# print(filterData)

	if filterData:
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
		# print(data)
		return Response(
				response=json.dumps({"data": data}),
				status=200,
				content_type='application/json'
			)

	else:
		return Response(
				response=json.dumps({
					"error": "true",
					"message": "景點編號不正確"
				}),
				status=400,
				content_type='application/json'
			)

	return Response(
				response=json.dumps({
					"error": "true",
					"message": "系統錯誤"
				}),
				status=500,
				content_type='application/json'
			)