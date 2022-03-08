'''
gate_face_k11_gz	mysql57.rdsm7gwoyphq7s0.rds.su.baidubce.com		gate_face_k11_gz:gate_face_k11_gz_yMZJAcf

k11_web_hl	172.20.10.20	root	bjuqjaJu72AupvEW4IuNULYYYjIdYXc9

gate_face_k11_gz	mysql57.rdsm7gwoyphq7s0.rds.su.baidubce.com	gate_face_k11_gz	gate_face_k11_gz_yMZJAcf

face_gate	mysql57.rdsmg8p7vvpm30x.rds.su.baidubce.com	face_gate	ZmoFfCrygDYFcPnc0xmi
UserPassword = "face_gate:ZmoFfCrygDYFcPnc0xmi"
    HostPort = "tcp(mysql57.rdsmg8p7vvpm30x.rds.su.baidubce.com:3306)"
    DB = "face_gate"
中关村壹号项目所在的数据库
'''


class Var:
	HOST = ""
	USERNAME = ""
	USERPASS = ""
	DBNAME = ""
	SQL = ""
	PATH = ""
	FILENAME = ""

	# test
	def gateface_test(self, project_id, createAtA, createAtB, page, limit):
		self.HOST = "172.20.10.20"
		self.USERNAME = "root"
		self.USERPASS = "bjuqjaJu72AupvEW4IuNULYYYjIdYXc9"
		self.DBNAME = "gate_face_hl"
		self.SQL = "SELECT * FROM match_logs WHERE type = 'image' and project_id = '" + project_id \
		           + "' AND created_at > '2021-" + createAtA + "' AND created_at < '2021-" + createAtB + "' ORDER BY created_at ASC LIMIT " + page + "," + limit
		print(self.SQL)

	# k11gz、k11tj、k11sh
	def gateface_k11(self, project_id, group_id, createAtA, createAtB, page, limit):
		self.HOST = "mysql57.rdsm7gwoyphq7s0.rds.su.baidubce.com"
		self.USERNAME = "gate_face_k11_gz"
		self.USERPASS = "gate_face_k11_gz_yMZJAcf"
		self.DBNAME = "gate_face_k11_gz"
		self.SQL = "SELECT * FROM match_logs WHERE type = 'image' AND project_id = '" + project_id \
		           + "' AND group_id like '" + group_id + "%' AND created_at > '2021-" + createAtA + "' AND created_at < '2021-" + createAtB + "' ORDER BY created_at ASC LIMIT " + page + "," + limit
		print(self.SQL)

	# zgcyh
	def gateface_other(self, project_id, createAtA, createAtB, page, limit):
		self.HOST = "mysql57.rdsmg8p7vvpm30x.rds.su.baidubce.com"
		self.USERNAME = "face_gate"
		self.USERPASS = "ZmoFfCrygDYFcPnc0xmi"
		self.DBNAME = "face_gate"
		self.SQL = "SELECT * FROM match_logs WHERE type = 'image' and project_id ='" + project_id \
		           + "' AND created_at > '2021-" + createAtA + "' AND created_at < '2021-" + createAtB + "'  ORDER BY created_at ASC LIMIT " + page + "," + limit
		print(self.SQL)

	# tygjq、hgsjq
	def sendinfo_bjdb(self, group_id, createAtA, createAtB, page, limit):
		self.HOST = "180.76.237.237"
		self.USERNAME = "sendinfo_read"
		self.USERPASS = "49cwAlpqbxL9BSTI6elp"
		self.DBNAME = "sendinfo"
		self.SQL = "SELECT * FROM match_logs WHERE group_id = '" + group_id \
		           + "' AND created_at > '2021-" + createAtA + "' AND created_at < '2021-" + createAtB + "' ORDER BY created_at ASC LIMIT " + page + "," + limit
		print(self.SQL)

	# tygjq、hgsjq
	def sendinfo_szdb(self, group_id, createAtA, createAtB, page, limit):
		self.HOST = "106.12.176.14"
		self.USERNAME = "sendinfo_read"
		self.USERPASS = "UrhMEJMl4G83AYV7Ep1ozaQ89UtBCTF9"
		self.DBNAME = "sendinfo"
		self.SQL = "SELECT * FROM match_logs WHERE group_id = '" + group_id \
		           + "' AND created_at > '2021-" + createAtA + "' AND created_at < '2021-" + createAtB + "' ORDER BY created_at ASC LIMIT " + page + "," + limit
		print(self.SQL)

	# 龙岩1011，烂苹果乐园1015，上海野生动物园1162，海昌1023，AibeeOfficeGate，山东水浒好汉城201801221755
	def sendinfo_stage2_db(self, group_id, createAtA, createAtB, page, limit):
		self.HOST = "mysql57.rdsmn0ym2ucmt9l.rds.su.baidubce.com"
		self.USERNAME = "sendinfo_stage_2"
		self.USERPASS = "o!cZ#0#TkMS1qhX1"
		self.DBNAME = "sendinfo_stage_2"
		self.SQL = "SELECT * FROM match_logs WHERE group_id = '" + group_id \
		           + "' AND created_at like '2021-" + createAtA + " %'  ORDER BY created_at ASC LIMIT " + page + "," + limit
		print(self.SQL + "")

	#sendinfo-web-stage，1089，1126，1017，1031，201709151420，201711211750，1219，1379572556，201804091822，test0428
	def sendinfo_mask_stage_db(self, group_id, createAtA, createAtB, page, limit):
		self.HOST = "106.12.176.14"
		self.USERNAME = "sendinfo_stage_r"
		self.USERPASS = "go9!Tu2pAcw%Cf2KgF#hnTwU"
		self.DBNAME = "sendinfo_stage"
		self.SQL = "SELECT * FROM match_logs WHERE group_id = '" + group_id \
		           + "' AND created_at > '2021-" + createAtA + "' AND created_at < '2021-" + createAtB + "' ORDER BY created_at ASC LIMIT " + page + "," + limit
		print(self.SQL)
