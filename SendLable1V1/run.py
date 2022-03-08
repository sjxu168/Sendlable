import sys
import time

from handleData import k11_get_img_from_matchlog_json
from handleData import sendinfobj_get_img_from_matchlog_json
from handleData import zgcyh_get_img_from_matchlog_json, sendinfosz_get_img_from_matchlog_json
from upload_download import localtoremote
from util import SqlUtil
from util.DataUtil import sqldata
from util.helpUtil import write_csv

'''
运行前检查
1.调用的数据库连接方法是否正确
2.sql查询语句的查询时间
3.文件名称、文件路径
'''


class SendLable:
	var = SqlUtil.Var()
	filetime = time.strftime("%Y%m%d", time.localtime())
	fname = None

	# 根据输入内容查询数据库内容
	def getData(self, projectid, startAT, endAT, page, limit):

		# 每次运行需要确定连接的数据库是否正确,项目ID，数据日期
		if projectid == "k11_sy":  # k11沈阳

			self.var.gateface_k11("k11_sy", "sy_", startAT, endAT, page, limit)
		# break
		elif projectid == "k11_gz":  # k11广州

			self.var.gateface_k11("k11_inland", "gz_", startAT, endAT, page, limit)
		# break
		elif projectid == "k11_sh":  # k11上海

			self.var.gateface_k11("k11_inland", "sh_", startAT, endAT, page, limit)
		# break
		elif projectid == "k11_tj":  # k11天津

			self.var.gateface_k11("k11_tj", "tj_", startAT, endAT, page, limit)
		# break
		elif projectid == "zgcyh_jq":  # 中关村壹号

			self.var.gateface_other("zgcyh_jq", startAT, endAT, page, limit)
		# break
		elif projectid == "1021" or projectid == "bj_hgs":  # 黄果树

			self.var.sendinfo_bjdb("1021", startAT, endAT, page, limit)
		# break
		elif projectid == "1188" or projectid == "sz_tmh":  # 天目湖

			self.var.sendinfo_szdb("1188", startAT, endAT, page, limit)
		# break
		elif projectid == "1124" or projectid == "sz_jgs":  # 井冈山

			self.var.sendinfo_szdb("1124", startAT, endAT, page, limit)
		# break
		elif projectid == "1214" or projectid == "bj_tyg":  # 天元谷

			self.var.sendinfo_bjdb("1214", startAT, endAT, page, limit)
		# break
		elif projectid == "1011" or projectid == "stage_ly":  # 龙岩

			self.var.sendinfo_stage2_db("1011", startAT, endAT, page, limit)
		# break
		elif projectid == "1015" or projectid == "stage_lpg":  # 烂苹果乐园

			self.var.sendinfo_stage2_db("1015", startAT, endAT, page, limit)
		# break
		elif projectid == "1162" or projectid == "stage_shdwy":  # 上海野生动物园

			self.var.sendinfo_stage2_db("1162", startAT, endAT, page, limit)
		# break
		elif projectid == "1023" or projectid == "stage_hc":  # 海昌

			self.var.sendinfo_stage2_db("1023", startAT, endAT, page, limit)
		# break
		elif projectid == "AibeeOfficeGate" or projectid == "stage_AibeeOfficeGate":  # 测试景区

			self.var.sendinfo_stage2_db("AibeeOfficeGate", startAT, endAT, page, limit)
		# break
		elif projectid == "201801221755" or projectid == "stage_hhc":  # 山东水浒好汉城

			self.var.sendinfo_stage2_db("201801221755", startAT, endAT, page, limit)
		# break
		elif projectid == "201710121749" or projectid == "sz_kly":  # 深大恐龙园

			self.var.sen("201710121749", startAT, endAT, page, limit)
		# break
		elif projectid == "1379572556" or projectid == "sz_gps":  # 深大恐龙园

			self.var.sendinfo_mask_stage_db("1379572556", startAT, endAT, page, limit)
		# break
		else:
			print("project_id输入有误，请重新输入！\n")
		# break
		mysql = sqldata(self.var.HOST, self.var.USERNAME, self.var.USERPASS, self.var.DBNAME)
		mysql.mysql2json(self.var.SQL, "./sql_file/", str(projectid) + "_" + self.filetime)
		return projectid, "./sql_file/" + str(projectid) + "_" + str(self.filetime) + ".json"

	# 根据查询出的sql结果下载图片
	def sql2img(self, projectid, createdAT, endAT, page, limit):
		pid, jdata = self.getData(projectid, createdAT, endAT, page, limit)
		# print(jdata)
		if pid in ["k11_sy", "k11_gz", "k11_sh", "k11_tj"]:
			self.fname = pid + "_" + self.filetime
			on_line_checkA = k11_get_img_from_matchlog_json.OnlineCheck(self.fname)
			on_line_checkA.GetImgFromMatchLogFile(jdata)
		elif pid in ["1188", "1124", "201710121749","1379572556", "sz_tmh", "sz_jgs", "sz_kly","sz_gps"]:
			# print('sdfdsfdsfdsfd')
			self.fname = pid + "_" + self.filetime
			# print('self.fname:%s' % self.fname)
			on_line_checkC = sendinfosz_get_img_from_matchlog_json.OnlineCheck(self.fname)
			on_line_checkC.GetImgFromMatchLogFile(jdata)
		elif pid in ["1021", "1214", "bj_tyg", "bj_hgs"]:
			self.fname = pid + "_" + self.filetime
			on_line_checkC = sendinfobj_get_img_from_matchlog_json.OnlineCheck(self.fname)
			on_line_checkC.GetImgFromMatchLogFile(jdata)
		elif pid in ["1011", "stage_ly", "1015", "stage_lpg", "1162", "stage_shdwy", "1023", "stage_hc",
		             "AibeeOfficeGate", "201801221755", "stage_hhc"]:
			self.fname = pid + "_" + self.filetime
			on_line_checkC = sendinfosz_get_img_from_matchlog_json.OnlineCheck(self.fname)
			on_line_checkC.GetImgFromMatchLogFile(jdata)
		elif pid in ["zgcyh_jq"]:
			self.fname = pid + "_" + self.filetime
			on_line_checkB = zgcyh_get_img_from_matchlog_json.OnlineCheck(self.fname)
			on_line_checkB.GetImgFromMatchLogFile(jdata)
		else:
			print("project_id输入有误，请重新输入！\n")


# #创建送标文件夹
# 	def mdirectory(self):
# 		filepath = "./data_last/T21imgs_TOURISM_general_general_"+self.fname
# 		oldpath = "./data_result/"+self.fname
# 		yamlpath = "./config/config.yaml"
# 		if not os.path.exists(filepath):
# 			os.makedirs(filepath)
# 		shutil.copy(yamlpath, filepath)
# 		shutil.move(oldpath, filepath)


if __name__ == '__main__':
	slable = SendLable()
	# parser = argparse.ArgumentParser(description='请输入要导出的项目名：\nk11_sy\nk11_gz\nk11_sh\nk11_tj\nzgcyh_jq\n黄果树:1021\n天目湖:1188\n井冈山:1124\n北京-天元谷:1214\n如：沈阳 \ 1021')
	# parser.add_argument('--project', type=str, required=True, help='请输入要导出的项目名：\nk11_sy\nk11_gz\nk11_sh\nk11_tj\nzgcyh_jq\nbj_hgs\nsz_tmh\nsz_jgs\nbj_tyg\n如：k11_sy')
	# parser.add_argument('--createdat', type=str, required=True, help='请输入开始日期，如06-12\n')
	# parser.add_argument('--endat', type=str, required=True, help='请输入结束日期，如06-12\nd')
	# parser.add_argument('--limit', type=str, required=True, help='请输入要导出的数据条数，如：1000\n')
	# args = parser.parse_args()
	project_id = sys.argv[1]  # project_id 项目ID，下拉选框，默认【】
	startAT = sys.argv[2]  # create_at 开始日期，输入框，默认08-19
	endAT = sys.argv[3]  # end_at 结束日期，输入框，默认08-20
	limit = sys.argv[4]  # limit 导数据条数，输入框，默认1500
	page = str(0)
	slable.sql2img(project_id, startAT, endAT, page, limit)
	dir = "/opt/jenkins/workspace/poc/sendlabel1v1/SendLable1V1/data_last/"
	reg_name = "T21imgs_TOURISM_general_general_"
	full_name = reg_name + slable.fname

	#print("run----------",dir + full_name + "/" + slable.fname)

	localtoremote.uploadGPU(dir + full_name)
	write_csv(dir+full_name + "/" + slable.fname,
	          "/data/gate_qa_tools/BenchmarkServer/tree/static/bench_mark_image/CsvFile/" + full_name + ".csv",
	          "FolderName,MatchScore,ThresholdScoren")
	# write_csv(dir + full_name + "/" + slable.fname,
	#           "./" + full_name + ".csv",
	#           "FolderName,MatchScore,ThresholdScoren")
	
# pass
