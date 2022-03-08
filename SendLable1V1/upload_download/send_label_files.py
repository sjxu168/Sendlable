import json
import os

import requests


# from upload_download.feishu_notification import send_feishu_text_message


class LabelSender:

	def copy_label_file_to_pangu(self, filename):

		"""
		将标注文件拷贝到天津服务器上
		:param data_dir:
		:return:
		"""
		cmd = 'ssh-keyscan 172.20.10.195>> ~/.ssh/known_hosts'
		exitcode = os.system(cmd)
		bash_cmd = f"sshpass -p 'abc123$%^' rsync -avP --delete --force {'/bj_dev/prod/QA/tmp/' + filename + '.tar'} " \
		           f"pangu@172.20.10.195:/home/pangu/T21imgs/"

		# transport = paramiko.Transport(('172.20.10.195', 22))
		# transport.connect(username='pangu', password='abc123$%^')
		# ssh = paramiko.SSHClient()
		# ssh._transport = transport
		# ssh.exec_command('scp ')

		exitcode = os.system(bash_cmd)
		print(exitcode)

	def create_label_task(self, filename):
		url = "https://pangu.aibee.cn/function/luban-send-label-service/jobs"  # 盘古线上环境地址
		label_rules = """
                标注规则：

                标注图片是否为同一个人。

                左右摇头：看不到一只眼睛，俯视：看不到嘴巴，仰视：看不到眼睛，则不选择

                遮挡较为严重的删除，如下图：[出现类似不符合要求的图片，即使可以看出和主图是同一个人，也不选择。如果主图也不符合要求，则什么都不选]
                """

		headers = {
			'content-type': "application/json",
			'cache-control': "no-cache"
		}
		params = {
			"tool_type": "T21imgs",  # 工具类型
			"path": filename,
			# 数据路径172.20.10.195服务器目录下文件夹名称, XXX_ignore_area比如全路径为 /home/first_party/Graphics/XXX_ignore_area, path为 XXX_ignore_area
			"customer": "TOURISM",  # customer, 全部大写英文字符
			"city": "general",  # city, 全部小写英文字符
			"store": "general",  # store, 全部小写英文字符
			"label_rules": label_rules,  # 标注说明, 按照markdown格式存储
			"fields_definition": {},  # 标注配置, 参考http://wiki.aibee.cn/pages/viewpage.action?pageId=18856332
			"submitter_id": "1662",  # 送标人用户id,默认1662是qa_sendlabel账号的userid
			"task_type": "labeler"  # task_type，任务类型，自己标注：self，标注员标注：labeler
		}

		send_label_response = requests.post(url=url, data=json.dumps(params), headers=headers)

		# print(send_label_response.json())

		task_id = send_label_response.json()['data']['id']
		task_name = send_label_response.json()['data']['path']
		if send_label_response.json()['error_no'] == 0:
			print("送标1个任务: \nID:" + str(task_id) + "，任务名称：" + task_name + "," + "\n辛苦审核标注，谢谢~")
		# send_feishu_text_message("jbzhou","sjxu", "yliu","送标1个任务: \nID:"+str(task_id)+"，任务名称："+task_name+","+"\n辛苦审核标注，谢谢~","nany")
		else:
			print("create task failed !!")

	def main(self, filename):
		# self.copy_label_file_to_pangu(filename)
		self.create_label_task(filename)
