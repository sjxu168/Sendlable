import os
import shutil

from upload_download.send_label_files import LabelSender


# https://www.jianshu.com/p/c692b82cb628下载安装sshpass

# 创建送标文件夹
def mdirectory(fname):
	filepath = "/opt/jenkins/workspace/poc/sendlabel1v1/SendLable1V1/data_last/T21imgs_TOURISM_general_general_" + fname
	oldpath = "/opt/jenkins/workspace/poc/sendlabel1v1/SendLable1V1/data_result/" + fname
	yamlpath = "/opt/jenkins/workspace/poc/sendlabel1v1/SendLable1V1/config/config.yaml"
	if not os.path.exists(filepath):
		os.makedirs(filepath)
	shutil.move(oldpath, filepath)
	shutil.copy(yamlpath, filepath)
	return fname


# 输入需要上传的文件路径，登录gpu服务，上传至pangu
def uploadGPU(filename):
	# 创建送标文件T21imgs_TOURISM_general_general_sql_fname存放data_last目录
	mdirectory(filename.split("_")[-3] + "_" + filename.split("_")[-2] + "_" + filename.split("_")[-1])
	bash_cmd = f"sshpass -p 'abc123$%^' rsync -avP {filename} pangu@172.20.10.195:/home/pangu/T21imgs/"
	os.system(bash_cmd)

	sender = LabelSender()
	sender.main(filename.split("/")[-1])

# if __name__ == '__main__':
# 	dir = "/Volumes/DocFile/PycharmProject/SendLabel/handleData/data_last/"
#
# 	filename = find_new_file(dir)
# 	if len(filename)>0:
# 		for f in filename:
# 			uploadGPU(dir)
