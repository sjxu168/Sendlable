#!/usr/bin/python
# coding=utf-8

import datetime
import json
import os
import time
from multiprocessing import Pool

import requests
from tqdm import tqdm

from handleData import del_only_one_img

ITEM_ID = 0  # "id"
ITEM_CREATED_TIME = 1  # created_at
# ITEM_USER_ID = 5  #
ITEM_IMG_URL = 9  # k11_image_url,bj_photo_url
# ITEM_MATCH_SCORE = 9  #
ITEM_THRESHOLD_SCORE = 12  # bj_score
ITEM_N_MATCH = 16  # top_n_match

ITEM_DEL_MARK = -1
VALUE_DEL_MARK = -1
THRESHOLD_SCORE = 90  # bj_match
CHECK_TOP_N = 1


class OnlineCheck:
	threshold_score = THRESHOLD_SCORE
	match_event_time = 3

	def __init__(self, PROJECT_NAME):
		self.PROJECT_NAME = PROJECT_NAME
		self.RESULT_IMG_DIR = "./data_result/{}/".format(self.PROJECT_NAME)

	def GetImgFromMatchLogFile(self, file_path):
		match_log = self.ReadMatchlogFile(file_path)
		match_event = self.FilterMatchEvent(match_log, THRESHOLD_SCORE)
		self.GetImgFromMatchlog(match_event)

	def ReadMatchlogFile(self, file_dir):
		list_match_logs = []
		with open(file_dir, 'rb+') as fp:
			reader = json.load(fp)
			for line in reader:
				line_list = list(line.values())  # dictionary转list
				line_list.append(0)  # 末尾增加对象-标记同一人多次比对尝试
				list_match_logs.append(line_list)
		return list_match_logs

	def GetMatchInfo(self, list_log):

		# topnmatch = list_log[ITEM_N_MATCH]
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
		size = len(list_match_logs)
		for i in range(0, size):
			current_log = list_match_logs[i]
			if threshold_score == 0:
				self.threshold_score = int(current_log[ITEM_THRESHOLD_SCORE])
			else:
				current_log[ITEM_THRESHOLD_SCORE] = str(threshold_score)

			if int(current_log[ITEM_DEL_MARK]) == VALUE_DEL_MARK:  # 验证重复时，标记为del
				continue

			if self.GetMatchInfo(current_log)[1] < self.threshold_score:  # 比对失败
				# 判断3s内有无重复尝试
				str_start_time = current_log[ITEM_CREATED_TIME]
				n_start_time_s = self.TransTime(str_start_time)
				repeat = False
				end_log = []
				for ii in range(i + 1, size):
					next_log = list_match_logs[ii]
					n_time_s = self.TransTime(next_log[ITEM_CREATED_TIME])
					if n_time_s < n_start_time_s:
						print("时间排序出错！")
						return
					if n_time_s > n_start_time_s + self.match_event_time:  # 超过3s
						if repeat is False:
							match_event.append(current_log)
						else:
							match_event.append(end_log)
							repeat = False
						break
					else:
						# 3s内出现同样的user_id,无论成功与否，都忽略当前log (连续识别成同一人，分值不会太低)
						if self.GetMatchInfo(next_log)[0] == self.GetMatchInfo(current_log)[0]:
							# if next_log[ITEM_USER_ID] == current_log[ITEM_USER_ID]:
							repeat = True
							if self.GetMatchInfo(current_log)[1] >= self.threshold_score:  # 遇到比对成功，直接结束
								break
							end_log = next_log
							next_log[ITEM_DEL_MARK] = str(VALUE_DEL_MARK)  # 标记为del

				# 只要3s内存在再次比对，无论成功与否，都删除当前log
				# 不做比对照之间验证了，因为到这一步比对成不同人，分值比较低，大概率是未注册，只影响误识统计（误识按攻击次数统计也合理）
				# if self.Compare2Images(next_log[ITEM_IMG_URL],current_log[ITEM_IMG_URL]):
				#     break

			else:  # 比对成功的，直接认为是一次match event
				match_event.append(current_log)

		return match_event

	def TransTime(self, str_time):
		return time.mktime(time.strptime(str_time, "%Y-%m-%d %H:%M:%S"))

	def TransTimeFormat(self, str_time):
		time_n = self.TransTime(str_time)
		time_l = time.localtime(time_n)
		#        return time.strftime("%Y%m%d%H%M%S", time_l)
		return time.strftime("%m%d%H%M%S", time_l)

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
		# for log in tqdm(match_event):
		if not os.path.exists(self.RESULT_IMG_DIR):
			os.makedirs(self.RESULT_IMG_DIR)
		with Pool(10) as p:
			p.map(self.multiprocess, tqdm(match_event))

		print('文件下载完成!')

		del_only_one_img.deleteone(self.RESULT_IMG_DIR)

		return 1

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
