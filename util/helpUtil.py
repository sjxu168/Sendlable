#!/usr/bin/env python
'''
@File : helpUtil.py
@Author : sjxu
@Date : 2021/7/5 下午2:34
@Content : 
'''
import csv
import os


def find_new_file(dir):
	'''查找目录下最新的文件'''
	os.system('find ./data_last/ -name ".DS_Store" -type f -delete')
	os.system(
		'find /opt/jenkins/workspace/poc/callresult1v1/SendLable1V1/mark_result/ -name ".DS_Store" -type f -delete')

	file_lists = os.listdir(dir)
	file_lists.sort(key=lambda fn: os.path.getatime(dir + "/" + fn))
	for filename in file_lists:
		print("f: ", filename, os.path.getatime(dir + "/" + filename))
		if filename.startswith("."):
			file_lists.remove(filename)
	file1 = os.path.join(dir, file_lists[-1])
	newfile = []
	newfile.append(file1)
	return newfile


def get_folder_data(folders):
	folder_res_list = []
	list_dirs = os.walk(folders)
	# print(list_dirs)
	for root, dirs, files in list_dirs:
		folder_dict = {}
		each_folder_res = {}
		# print(root)
		# print(files)
		if len(files) != 0:
			folder_names = root.split('/')[-1]
			for i in range(len(files)):
				if files[i].endswith('.jpg'):
					if files[i].startswith('00-'):
						threshold = files[i].split('_')[-1].strip('.jpg')
						each_folder_res['threshold'] = threshold
					else:
						scores = files[i].split('_')[1]
						each_folder_res['score'] = scores
						folder_dict[folder_names] = each_folder_res
						folder_res_list.append(folder_dict)
				else:
					pass
	# print(folder_res_list)
	return folder_res_list


def write_csv(folders, file_csv_path, table_header):
	folder_res_list = get_folder_data(folders)
	# print(len(folder_res_list))
	# 1. 创建文件对象
	f = open(file_csv_path, 'w', encoding='utf-8')
	# 2. 基于文件对象构建 csv写入对象
	csv_writer = csv.writer(f)
	# 3. 构建列表头
	table_header_list = table_header.split(',')
	csv_writer.writerow(table_header_list)
	# 4. 将内容写入csv文件
	for i in range(len(folder_res_list)):
		# print(folder_res_list[i])
		each_folder_dict = folder_res_list[i]
		for key in each_folder_dict:
			file_dict = each_folder_dict[key]
			csv_writer.writerow([key, file_dict['score'], file_dict['threshold']])
	# 5. 关闭文件
	f.close()
	print("csv文件创建完成！\n点击 http://172.16.16.30:8088/static/bench_mark_image/CsvFile/" + folders.split("/")[
		-2].strip() + ".csv 下载文件")
# if __name__ == '__main__':
#     write_csv("./data_last/T21img_TOURISM_general_general_zgcyh_jq_20210825")
