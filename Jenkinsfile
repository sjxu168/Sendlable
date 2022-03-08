pipeline {
    agent {
        node 'gpu480'
    }
    environment {
        PYTHONIOENCODING='utf-8'
        PYTHONPATH = '.'
    }
    parameters{
    choice(name: 'project_id', choices: ['k11_sy', 'k11_tj', 'k11_sh', 'k11_gz','zgcyh_jq','sz_tmh','sz_jgs', 'sz_kly','sz_gps','bj_hgs','bj_tyg'],description: '选择要送标的项目ID')
    string(name: 'createdat', defaultValue: '08-19', description: '数据起始时间', trim: true)
    string(name: 'endat', defaultValue: '08-20', description: '数据结尾时间', trim: true)
    string(name: 'limit', defaultValue: '10', description: '数据下载条数', trim: true)
    }
//python3 local_run.py true 08-19 08-20 10 true ./sql_file/matchlog_zgcyh_20210623.json true ./data_last/T21imgs_TOURISM_general_general_zgcyh_20210623 true T21imgs_TOURISM_general_general_zgcyh_20210623
    stages {
        stage('Build') {
            steps {
                dir('/opt/jenkins/workspace/poc/sendlabel1v1/SendLable1V1') {
                    sh('whoami')
                    sh('pwd')
                    sh('export PYTHONPATH=.')
                    sh('export PYTHONIOENCODING=utf-8')
                    sh('PYTHONIOENCODING=utf-8 python3 run.py ${project_id} ${createdat} ${endat} ${limit}')
                }
            }
        }
    }
}
