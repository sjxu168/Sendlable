import os
import sys
import time

from handleData import k11_get_img_from_matchlog_json
from handleData import sendinfobj_get_img_from_matchlog_json
from handleData import zgcyh_get_img_from_matchlog_json, sendinfosz_get_img_from_matchlog_json
from upload_download import localtoremote
from upload_download.send_label_files import LabelSender
from util import SqlUtil
from util.DataUtil import sqldata
from util.helpUtil import write_csv

'''
运行前检查
1.调用的数据库连接方法是否正确
2.sql查询语句的查询时间
3.文件名称、文件路径
'''

if __name__ == '__main__':

	is_select = sys.argv[1]  # true/false 是否需要查询数据，默认【true】
	project_id = sys.argv[2]  # project_id 项目ID，下拉选框，默认【】
	startAT = sys.argv[3]  # create_at 开始日期，输入框，默认08-19
	endAT = sys.argv[4]  # end_at 结束日期，输入框，默认08-20
	page = str(0)  # 页码
	limit = sys.argv[5]  # limit 导数据条数，输入框，默认1500
	is_download = sys.argv[6]  # true/false 是否需要下载图片，默认【true】
	sql_path = sys.argv[7]  # 自定义，下载后图片存放的目录名
	is_upload = sys.argv[8]  # true/false 是否需要上传图片，默认【true】
	T21imgs_path = sys.argv[9]  # 自定义，需要上传的T21imgs的图片路径
	is_send = sys.argv[10]  # true/false 是否需要送标，默认【true】
	T21imgs_name = sys.argv[11]  # 自定义，送标的T21imgs的图片名称

	new_sql_fnames = project_id + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime())  # 文件名格式 group_id+当前日期

	# 第一步：1.查询数据库数据(调用的方法不同，参数也不同)，参数【项目ID/groupid/开始日期/结束日期/数据条数】，输出【json文件】存放到sql_file
	# 连接数据库
	if is_select == 'true':
		print("-------------开始查询数据-----------------")
		var = SqlUtil.Var()
		group_id = project_id.split("_")[-1] + "_"
		if project_id == "k11_sy":  # k11沈阳
			var.gateface_k11(project_id, group_id, startAT, endAT, page, limit)
		elif project_id == "k11_tj":  # k11天津
			var.gateface_k11(project_id, group_id, startAT, endAT, page, limit)
		elif project_id == "k11_gz":  # k11广州
			var.gateface_k11("k11_inland", group_id, startAT, endAT, page, limit)
		elif project_id == "k11_sh":  # k11上海
			var.gateface_k11("k11_inland", group_id, startAT, endAT, page, limit)
		elif project_id == "zgcyh_jq":  # 中关村壹号
			var.gateface_other(project_id, startAT, endAT, page, limit)
		elif project_id == "bj_hgs":  # 黄果树
			var.sendinfo_bjdb("1021", startAT, endAT, page, limit)
		elif project_id == "sz_tmh":  # 天目湖
			var.sendinfo_szdb("1188", startAT, endAT, page, limit)
		elif project_id == "sz_jgs":  # 井冈山
			var.sendinfo_szdb("1124", startAT, endAT, page, limit)
		elif project_id == "bj_tyg":  # 天元谷
			var.sendinfo_bjdb("1214", startAT, endAT, page, limit)
		elif project_id == "stage_ly":  # 龙岩
			var.sendinfo_stage2_db("1011", startAT, endAT, page, limit)
		elif project_id == "stage_lpg":  # 烂苹果乐园
			var.sendinfo_stage2_db("1015", startAT, endAT, page, limit)
		elif project_id == "stage_shdwy":  # 上海野生动物园
			var.sendinfo_stage2_db("1162", startAT, endAT, page, limit)
		elif project_id == "stage_hc":  # 海昌
			var.sendinfo_stage2_db("1023", startAT, endAT, page, limit)
		elif project_id == "stage_AibeeOfficeGate":  # 测试景区
			var.sendinfo_stage2_db("AibeeOfficeGate", startAT, endAT, limit)
		elif project_id == "stage_hhc":  # 山东水浒好汉城
			var.sendinfo_stage2_db("201801221755", startAT, endAT, page, limit)
		elif project_id == "sz_kly":  # 深大恐龙园
			var.sendinfo_szdb("201710121749", startAT, endAT, page, limit)
		else:
			print("project_id输入有误，请重新输入！\n")

		mysql = sqldata(var.HOST, var.USERNAME, var.USERPASS, var.DBNAME)

		os.system("mv {0} {1}".format(os.path.join(sql_path, project_id + ".json"),
		                              os.path.join(sql_path, new_sql_fnames + ".json")))
		print(sql_path, project_id, sql_path, new_sql_fnames)
		# 数据格式转json文件
		mysql.mysql2json(var.SQL, sql_path, project_id)
		print("-------------数据导出成功-----------------")
	# 第二步，根据json文件下载图片存放到data_result
	if is_download == 'true':
		if is_select == 'false':
			sql_path = os.path.join(sql_path)
			fname = (sql_path.split("/")[-1]).split(".")[0]
		else:
			fname = project_id + "_" + time.strftime("%Y%m%d", time.localtime())
			# fpath = os.path.join(sql_path, project_id + '.json')
			sql_path = os.path.join(sql_path, project_id + '.json')
		print("-------------开始下载图片-----------------")
		if project_id in ["k11_sy", "k11_gz", "k11_sh", "k11_tj"]:
			on_line_checkA = k11_get_img_from_matchlog_json.OnlineCheck(fname)
			on_line_checkA.GetImgFromMatchLogFile(sql_path)
		elif project_id in ["1188", "1124", "201710121749", "sz_tmh", "sz_jgs", "sz_kly"]:
			on_line_checkC = sendinfosz_get_img_from_matchlog_json.OnlineCheck(fname)
			on_line_checkC.GetImgFromMatchLogFile(sql_path)
		elif project_id in ["1021", "1214", "bj_tyg", "bj_hgs"]:
			on_line_checkC = sendinfobj_get_img_from_matchlog_json.OnlineCheck(fname)
			on_line_checkC.GetImgFromMatchLogFile(sql_path)
		elif project_id in ["1011", "stage_ly", "1015", "stage_lpg", "1162", "stage_shdwy", "1023", "stage_hc",
		                    "AibeeOfficeGate", "201801221755", "stage_hhc"]:
			on_line_checkC = sendinfosz_get_img_from_matchlog_json.OnlineCheck(fname)
			on_line_checkC.GetImgFromMatchLogFile(sql_path)
		elif project_id in ["zgcyh_jq"]:
			on_line_checkB = zgcyh_get_img_from_matchlog_json.OnlineCheck(fname)
			on_line_checkB.GetImgFromMatchLogFile(sql_path)
		else:
			print("project_id输入有误，请重新输入！\n")
		print("-------------图片下载成功-----------------")

	# 第三步，打包并上传到盘古服务
	if is_upload == "true":
		print("-------------开始上传图片-----------------", sql_path)
		if is_select == 'false' and is_download == 'true':
			T21imgs_path = "./data_last/T21imgs_TOURISM_general_general_" + project_id + "_" + time.strftime("%Y%m%d",
			                                                                                                 time.localtime())
			localtoremote.uploadGPU(T21imgs_path)
		elif is_select == 'false' and is_download == 'false':
			T21imgs_path = T21imgs_path
			localtoremote.uploadGPU(T21imgs_path.split("/")[-1])
		elif is_select == 'true' and is_download == 'false':
			T21imgs_path = T21imgs_path
			localtoremote.uploadGPU(T21imgs_path.split("/")[-1])
		else:
			T21imgs_path = "./data_last/T21imgs_TOURISM_general_general_" + project_id + "_" + time.strftime("%Y%m%d",
			                                                                                                 time.localtime())
			localtoremote.uploadGPU(T21imgs_path)
		print("-------------图片上传成功-----------------")
		# write_csv(T21imgs_path+"/"+T21imgs_path.split("_")[-3].strip()+"_"+T21imgs_path.split("_")[-2].strip()+"_"+T21imgs_path.split("_")[-1].strip(), "/data/gate_qa_tools/BenchmarkServer/tree/static/bench_mark_image/CsvFile/"+T21imgs_path.split("/")[-1].strip()+".csv", "FolderName,MatchScore,ThresholdScoren")
		write_csv(
			T21imgs_path + "/" + T21imgs_path.split("_")[-3].strip() + "_" + T21imgs_path.split("_")[-2].strip() + "_" +
			T21imgs_path.split("_")[-1].strip(), "./" + T21imgs_path.split("/")[-1].strip() + ".csv",
			"FolderName,MatchScore,ThresholdScoren")

	# 第四步，创建送标任务
	if is_send == "true":
		print("-------------开始创建送标任务-----------------")
		sender = LabelSender()
		if is_upload == "false":
			sender.main(T21imgs_name)
		else:
			print(T21imgs_path)
			sender.main(T21imgs_path.split("/")[-1])
		print("-------------送标任务创建成功-----------------")
