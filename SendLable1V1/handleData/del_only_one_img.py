#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import shutil

from tqdm import tqdm


def deleteone(data_dir):
	# data_dir = "./data_result/k11sh_20210612/"

	os.system("find {} -name \".DS_Store\" -type f -delete".format(data_dir))

	del_num = 0
	dirs = []
	for item in os.listdir(data_dir):
		if os.path.isdir(os.path.join(data_dir, item)):
			dirs.append(item)

	# print(len(dirs))
	for dir in tqdm(dirs):
		# print(dir)
		dir = os.path.join(data_dir, dir)
		if len(os.listdir(dir)) < 2:
			shutil.rmtree(dir)
			del_num += 1
			continue

		haveRegister = False
		for file in os.listdir(dir):
			if file.startswith('00-'):
				haveRegister = True
		if haveRegister is False:
			shutil.rmtree(dir)
			del_num += 1

	print("total delete dir {} 个".format(del_num))
	print(f"total num:{len(dirs) - del_num} 个")
