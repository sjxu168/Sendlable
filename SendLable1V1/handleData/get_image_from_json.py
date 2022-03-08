#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime
import json
import os
from multiprocessing import Pool

import requests
from tqdm import tqdm

from handleData import del_only_one_img

ITEM_ID = "id"
ITEM_CREATED_TIME = "created_at"
# k11
ITEM_IMG_URL = "image_url"
# sendinfo
ITEM_IMG_URL = "photo_url"
# sendinfo
ITEM_THRESHOLD_SCORE = "score"  # 阈值

ITEM_N_MATCH = "top_n_match"

THRESHOLD_SCORE = 90
CHECK_TOP_N = 1


class OnlineCheck:
	# threshold_score = THRESHOLD_SCORE

	# 初始化类时传参PROJECT_NAME：项目名
	def __init__(self, PROJECT_NAME):
		self.PROJECT_NAME = PROJECT_NAME
		self.RESULT_IMG_DIR = "./data_result/{}/".format(self.PROJECT_NAME)

	# file_path：文件路径 根据路径读取文件/读取数据
	def GetImgFromMatchLogFile(self, file_path):
		match_log = self.ReadMatchlogFile(file_path)
		match_event = self.FilterMatchEvent(match_log, THRESHOLD_SCORE)
		self.GetImgFromMatchlog(match_event)

	# 读取json文件，将所有match—log转为list
	def ReadMatchlogFile(self, file_dir):
		list_match_logs = []
		with open(file_dir, 'rb+') as fp:
			reader = json.load(fp)
			for line in reader:
				line_list = list(line.values())  # dictionary转list
				line_list.append(0)  # 末尾增加对象-标记同一人多次比对尝试
				list_match_logs.append(line_list)
		return list_match_logs

	# 读取
	def GetMatchInfo(self, list_log):
		if list_log[ITEM_N_MATCH] != 'null':
			dict = json.loads(list_log[ITEM_N_MATCH])
			size = len(dict)

			if size < 1:
				return None
			user_id = dict[0]["user_id"]
			match_score = dict[0]["score"]
			return (user_id, int(match_score))
		else:
			return None

	def FilterMatchEvent(self, list_match_logs, threshold_score=0):
		match_event = []
		for i in range(0, len(list_match_logs)):

			current_log = list_match_logs[i]
			if current_log[ITEM_N_MATCH] == 'null':
				continue
			if threshold_score == 0:
				self.threshold_score = int(current_log[ITEM_THRESHOLD_SCORE])
			else:
				current_log[ITEM_THRESHOLD_SCORE] = str(THRESHOLD_SCORE)

			match_event.append(current_log)

		return match_event

	def multiprocess(self, log):
		time_str = str(datetime.datetime.strptime(log[ITEM_CREATED_TIME], "%Y-%m-%d %H:%M:%S"))
		time_str = self.TransTimeFormat(time_str)
		img_name = "00-{}_{}.jpg".format(log[ITEM_ID], log[ITEM_THRESHOLD_SCORE])
		img_path = '{}/{}_{}'.format(self.RESULT_IMG_DIR, log[ITEM_ID], time_str)
		self.GetSearchPhoto(log[ITEM_IMG_URL], img_path, img_name)
		dict = json.loads(log[ITEM_N_MATCH])
		size = len(dict)
		if size > CHECK_TOP_N:
			size = CHECK_TOP_N
		for i in range(0, size):
			score = dict[i]["score"]
			img_match = dict[i]["image_url"]
			id = dict[i]["user_id"]
			img_name = "top{}_{}_{}.jpg".format(i + 1, score, id)
			self.GetSearchPhoto(img_match, img_path, img_name)
		return img_path.split("/")[-1] + "," + img_name.split(".")[0].split("_")[1] + "," + log[
			ITEM_THRESHOLD_SCORE] + "\n"

	def GetImgFromMatchlog(self, match_event):
		if not os.path.exists(self.RESULT_IMG_DIR):
			os.makedirs(self.RESULT_IMG_DIR)
		with Pool(10) as p:
			p.map(self.multiprocess, tqdm(match_event))
		print('文件下载完成!')
		del_only_one_img.deleteone(self.RESULT_IMG_DIR)

	def GetSearchPhoto(self, photo_url, img_path, img_name):
		if os.path.exists('{}/{}'.format(img_path, img_name)):
			return 1
		try:
			if not os.path.exists(img_path):
				os.makedirs(img_path)
		except:
			pass
		try:
			r = requests.get(photo_url, timeout=5)
		except:
			pass
		else:
			if r.status_code == requests.codes.ok:
				with open('{}/{}'.format(img_path, img_name), 'wb') as fp:
					fp.write(r.content)

		return 0

# if __name__ == "__main__":
#     on_line_check = OnlineCheck()
#     on_line_check.GetImgFromMatchLogFile(MATCH_LOG_FILE_DIR)
