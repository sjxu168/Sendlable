#!/usr/bin/env python
'''
@File : lj_run.py.py
@Author : sjxu
@Date : 2021/11/9 下午5:01
@Content : 
'''

import sys

from upload_download import localtoremote
from util.helpUtil import write_csv

if __name__ == '__main__':
	T21imgs_name = sys.argv[1]  # 自定义，需要上传的T21imgs的图片名称

	T21imgs_path = "/opt/jenkins/workspace/poc/sendlabel1v1/SendLable1V1/data_last/T21imgs_TOURISM_general_general_" + (
		T21imgs_name)
	localtoremote.uploadGPU(T21imgs_path)

	write_csv(
		T21imgs_path + "/" + T21imgs_path.split("_")[-3].strip() + "_" + T21imgs_path.split("_")[-2].strip() + "_" +
		T21imgs_path.split("_")[-1].strip(),
		"/data/gate_qa_tools/BenchmarkServer/tree/static/bench_mark_image/CsvFile/" + T21imgs_path.split("/")[
			-1].strip() + ".csv", "FolderName,MatchScore,ThresholdScoren")
# write_csv(T21imgs_path+"/"+T21imgs_path.split("_")[-3].strip()+"_"+T21imgs_path.split("_")[-2].strip()+"_"+T21imgs_path.split("_")[-1].strip(), "./"+T21imgs_path.split("/")[-1].strip()+".csv", "FolderName,MatchScore,ThresholdScoren")
