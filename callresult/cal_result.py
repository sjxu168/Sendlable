import argparse
import os
import shutil

from tqdm import tqdm

from upload_download import remotetolocal


# sys.path.append("../upload_download/localtoremote.py")

def collectDoubt(data):
	result_logs = []
	with open(data, 'r') as fp:
		lines = fp.readlines()
		for line in lines:
			list = line.split(',')
			length = len(list)
			if length > 1 and list[1].strip() != "":
				result_logs.append(list[1].strip())
	# print("result logs\n",result_logs)
	return result_logs


def analysis_result_file(data):
	result_logs = {}
	with open(data, 'r') as fp:
		lines = fp.readlines()
		for line in lines:
			list = line.split(',')
			length = len(list)
			if length > 1 and list[1].strip() != "":
				register_img = list[1].strip()
				i = 2
				match_img = []
				while (length > i and list[i].strip() != ""):
					match_img.append(list[i].strip())
					i += 1
				# if(len(match_img) != 0):
				result_logs[register_img] = match_img
	# print("result logs\n",result_logs)
	return result_logs


def deleteDir(data_dir):
	# data_dir = "../data_last/"
	dirs = []

	for item in os.listdir(data_dir):
		if os.path.isdir(os.path.join(data_dir, item)):
			dirs.append(item)
	for dir in tqdm(dirs):
		dir = os.path.join(data_dir, dir)
		shutil.rmtree(dir)
	print("提示：原始数据已清空！")
	return


def _cFile(fp, foldername, matchscore, threshold_score):
	fp.write(foldername + ",")
	fp.write(matchscore + ",")
	fp.write(threshold_score + "\n")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description='请输入要导出的文件名：')
	parser.add_argument('--filename', type=str, required=True,
	                    help='请输入要导出的文件名：')
	args = parser.parse_args()
	filename1 = args.filename
	# print(filename1)
	remotetolocal.connecthdfs(filename1)

	# filepath = find_new_file()[0]
	# filename1 =filepath.split("/")[-1]
	# print("file1  ",filename1)
	filename2 = filename1.split("_")[-3] + "_" + filename1.split("_")[-2] + "_" + filename1.split("_")[-1]
	# filename2 = filename1.split("_")[-2]+"_"+filename1.split("_")[-1]
	# print("file2  ", filename2)
	os.system('pwd')
	result_dir = "./mark_result/" + filename1 + "/" + filename1 + "_before_merge.txt"
	doubt_txt = "./mark_result/" + filename1 + "/" + filename1 + "_doubt.txt"
	origin_img_dir = "/opt/jenkins/workspace/poc/sendlabel1v1/SendLable1V1/data_last/" + filename1 + "/" + filename2
	result_img_dir = "/data/gate_qa_tools/BenchmarkServer/tree/static/bench_mark_image/" + filename2
	# print("result_dir--" + result_dir, "   origin_img_dir--" + origin_img_dir,
	#      "    result_img_dir--" + result_img_dir)

	score = 0
	FN = 0  # 漏识
	FP = 0  # 误识
	TP = 0  # 正识
	TN = 0  # 真的负
	Total = 0

	x_dict = analysis_result_file(result_dir)
	# print(x_dict)
	doubtList = collectDoubt(doubt_txt)
	# 创建结果统计文件夹
	if not os.path.exists(result_img_dir):
		os.makedirs(result_img_dir)
	FN_dir = "{}/FN".format(result_img_dir)
	if not os.path.exists(FN_dir):
		os.makedirs(FN_dir)
	FP_dir = "{}/FP".format(result_img_dir)
	if not os.path.exists(FP_dir):
		os.makedirs(FP_dir)
	TP_dir = "{}/TP".format(result_img_dir)
	if not os.path.exists(TP_dir):
		os.makedirs(TP_dir)
	TN_dir = "{}/TN".format(result_img_dir)
	if not os.path.exists(TN_dir):
		os.makedirs(TN_dir)
	doubt_dir = "{}/doubt".format(result_img_dir)
	if not os.path.exists(doubt_dir):
		os.makedirs(doubt_dir)

	ignore = 0
	# 按行遍历所有结果标注log
	for (root, dirs, files) in os.walk(origin_img_dir):
		for folder in tqdm(dirs):
			sub_folder = os.path.join(root, folder)
			for (root1, dirs1, files1) in os.walk(sub_folder):
				# print("sub-folder  ",sub_folder)
				register_img = ""
				match_imgs = []
				b_have_match = False
				i = 0
				for item in files1:  # 先确定注册照
					if item.startswith("00-"):
						# print("00 ",item)
						#if score == 0:
						score = int(item.split(".")[0].split("_")[-1])
						if item in x_dict:
							# print("here ", item)
							i = 1
							match_imgs = x_dict[item]
							b_have_match = True
							register_img = item
							break

				# register_img = item  #防止存在两张注册照"00-"
				# if "old" in origin_img_dir:
				for item in files1:
					target_dir = ""
					if item.startswith("TOP1") or item.startswith("top1"):
						# print("top ",item)
						Total += 1
						match_score = int(item.split("_")[1])
						if i != 0 and item in match_imgs:
							# print("have both ",item)
							if match_score >= score:  # 正识
								TP += 1
								target_dir = TP_dir
							else:  # 漏识
								FN += 1
								target_dir = FN_dir
						else:  # 误识
							if i == 0:
								ignore += 1
							# target_dir = doubt_dir
							# print("ignore----", ignore)
							else:
								# print("have one ",files1)
								if match_score >= score:
									FP += 1
									target_dir = FP_dir
								else:  # 未注册
									TN += 1
									target_dir = TN_dir
					if target_dir != "":
						target_folder = "{}/{}".format(target_dir, folder)
						# print(" target ", target_dir, "  folder ", target_folder)
						if not os.path.exists(target_folder):
							os.makedirs(target_folder)
						shutil.copyfile("{}/{}".format(sub_folder, item), "{}/{}".format(target_folder, item))
						shutil.copyfile("{}/{}".format(sub_folder, register_img),
						                "{}/{}".format(target_folder, register_img))

				# print("dir1 ",sub_folder)
				for item in files1:
					if item in doubtList:
						# print(sub_folder," to ","{}/{}".format(doubt_dir, folder))
						shutil.copytree(sub_folder, "{}/{}".format(doubt_dir, folder))

	print('the task is end')
	print('Total: ' + str(Total))
	print('正识TP: ' + str(TP))
	print('误识FP: ' + str(FP))
	print('漏识FN: ' + str(FN))
	print('未注册TN: ' + str(TN))
	print("ignore", ignore)
	# print('recall=%.4f   fnr=%.4f   fpr=%.4f' % (TP/(TP+FN), FN/(FN+TP), FP/(FP+TN)))
	print('recall=%.2f%%   fpr=%.2f%%' % (TP / (TP + FN) * 100, FP / (Total) * 100))
	print(filename2 + "的数据统计已完成！\n点击 http://172.16.16.30:8088/?fd=static/bench_mark_image/" + filename2 + " 查看图片")

# deleteDir("../data_last/")
# deleteDir("../mark_result/")
