#!/usr/bin/env python
'''
@File : remotetolocal.py
@Author : sjxu
@Time : 2021/6/18 下午5:06
'''

# 连接hdfs
import os


# import pexpect

# from aibee_hdfs import hdfscli
# from aibee_hdfs.hdfs.hdfs.util import HdfsError


def connecthdfs(filename):
	dir = "../data_last/"
	print(filename)

	keytab = './config/sjyw.keytab'
	username = 'sjyw'
	# print("test文件检查执行1... ... ")
	# use keytab

	os.system("/root/anaconda3/envs/aibee/bin/hdfscli initkrb5 -k " + keytab + " " + username)
	# print("test文件检查执行2... ... ")
	print("下载标注结果", filename)
	os.system(
		'/root/anaconda3/envs/aibee/bin/hdfscli download /bj/prod/label-platform/labeling_result/T21imgs/' + filename + " /opt/jenkins/workspace/poc/callresult1v1/SendLable1V1/mark_result/")
	print("标注结果已导出 ")


if __name__ == '__main__':
	connecthdfs()
