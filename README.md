# gate_qa_tools
some general tools for gate qa

Sendlable V2.0.0
2021-11-11
author:sjxu
 
常规景区送标：

	1.Jenkins一键运行，Buildwithparameter
		运行run.py文件
		如：python3 run.py sz_kly 10-20 10-31 3000

	2.参数介绍：
        --project_id "项目名"  #项目名：k11沈阳：k11_sy、k11广州：k11_gz、k11上海：k11_sh、k11天津：k11_tj、中关村壹号：zgcyh_jq、北京黄果树：bjhgs、苏州天目湖:sztmh、苏州井冈山：szjgs、北京天元谷：bjtyg
        --createdat "开始日期"  #开始日期：如：06-12
        --endat "结束日期"  #结束日期：如：06-15
        --limit "数据条数"  #数据条数：如：1000

	3.程序执行完成后，在Jenkins的job日志里打印出任务名称和编号
        注：每次运行run.py文件前，data_last目录下不能有重名文件夹，如有重复可删除历史图片目录
        路径：/opt/jenkins/workspace/poc/sendlabel1v1/SendLable1V1/data_last/

丽江景区送标：

    注：需提前将下载好的图片文件夹用远程工具上传到：root@gpu480.aibee.cn:/opt/jenkins/workspace/poc/sendlabel1v1/SendLable1V1/data_result/
    1.Jenkins一键运行，Buildwithparameter
		运行lj_run.py文件
		如：python3 lj_sendlable/lj_run.py li_jiang_00000000

	2.参数介绍：
        --foldername "下载图片名称"  #如：li_jiang_00000000

	3.程序执行完成后，在Jenkins的job日志里打印出任务名称和编号
        同常规景区

标注结果统计：

	1.Jenkins一键运行，Buildwithparameter
		运行cal_result.py文件
	2.参数介绍：
		--filename "文件名称"
		如：T21img_TOURISM_general_general_k11_tj_20210702（送标的任务名称）
	3.标注结果导出
		数据路径：root@gpu480.aibee.cn:/data/gate_qa_tools/BenchmarkServer/tree/static/bench_mark_image/
	4.图片查看可结合http://172.16.17.16:8088/图片标注工具查看

本地送标后jenkins统计结果：

    注：需提前将T21imgs_TOURISM_general_general_k11_tj_20210702文件夹上传到：root@gpu480.aibee.cn:/opt/jenkins/workspace/poc/sendlabel1v1/SendLable1V1/data_last/
    1.Jenkins一键运行，Buildwithparameter
		运行cal_result.py文件
	2.参数介绍：
		--filename "文件名称"
		如：T21img_TOURISM_general_general_k11_tj_20210702（送标的任务名称）
	3.标注结果导出
		数据路径：root@gpu480.aibee.cn:/data/gate_qa_tools/BenchmarkServer/tree/static/bench_mark_image/
	4.图片查看可结合http://172.16.17.16:8088/图片标注工具查看
