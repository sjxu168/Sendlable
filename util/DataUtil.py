#!/usr/bin/env python
# coding=utf-8

import json
import os
import time
from os import path

import pymysql

# 获取当前目录
d = path.dirname(__file__)


class sqldata():
	# 初始化函数，初始化连接列表
	def __init__(self, host, user, pwd, dbname):
		self.host = host
		self.user = user
		self.pwd = pwd
		self.dbname = dbname

	def getCursor(self):
		# 数据库连接重试功能和连接超时功能的DB连接
		_conn_status = True
		_max_retries_count = 10  # 设置最大重试次数
		_conn_retries_count = 0  # 初始重试次数
		_conn_timeout = 60  # 连接超时时间为3秒
		while _conn_status and _conn_retries_count <= _max_retries_count:
			try:
				print
				'连接数据库中..'
				self.db = pymysql.connect(host=self.host, user=self.user, password=self.pwd, database=self.dbname,
				                          connect_timeout=_conn_timeout, read_timeout=_conn_timeout)
				_conn_status = False  # 如果conn成功则_status为设置为False则退出循环，返回db连接对象
				# 创建游标对象
				cur = self.db.cursor()

				# 返回
				return cur
			except:
				_conn_retries_count += 1
				print
				_conn_retries_count
			print
			'connect db is error!!'
			time.sleep(3)  # 此为测试看效果
			continue

	# 查询操作
	def queryOperation(self, sql):
		# 建立连接获取游标对象
		cur = self.getCursor()

		# 执行SQL语句
		cur.execute(sql)

		# 获取数据的行数
		row = cur.rowcount

		# 获取查询数据
		# fetch*
		# all 所有数据,one 取结果的一行，many(size),去size行
		dataList = cur.fetchall()

		# 关闭游标对象
		cur.close()

		# 关闭连接
		self.db.close()

		# 返回查询的数据
		return dataList, row

	def create_folder(self, paths):
		# 如果目录不存在则创建
		if not os.path.exists(paths):
			os.makedirs(paths)
			print('创建目录：{0}成功！'.format(paths))
		else:
			print('目录：{0}已存在！'.format(paths))

	def mysql2json(self, sql, jsonPath, fileName):
		parent_path = os.path.dirname(d)
		jsonPath = os.path.join(parent_path, jsonPath)
		self.create_folder(jsonPath)
		jsonPath_name = os.path.join(jsonPath, fileName + '.json')
		print('jsonPath_name：{0}'.format(jsonPath_name))
		# 建立连接获取游标对象
		cur = self.getCursor()
		# 执行SQL语句
		cur.execute(sql)
		datas = cur.fetchall()
		fields = cur.description
		column_list = []
		column_lists = []
		for field in fields:
			column_list.append(field[0])

		# with open('{jsonPath}{fileName}.json'.format(jsonPath=jsonPath, fileName=fileName), 'w+') as f:
		with open(jsonPath_name, 'w+') as f:
			# f.write("[")
			i = 0
			for row in datas:
				result = {}
				for fieldIndex in range(0, len(column_list)):
					result[column_list[fieldIndex]] = str(row[fieldIndex])
				# jsondata = json.dumps(result)
				column_lists.append(result)
				i += 1
			# print(column_lists)
			f.write(json.dumps(column_lists, indent=4))

			# f.write(json.dumps(column_lists, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))

			# f.write("]")
			print("执行", sql, "\n共导出", i, "条数据")
		f.close()

		cur.close()
		self.db.close()
