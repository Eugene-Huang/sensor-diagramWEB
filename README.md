# sensor-diagramWEB

## 项目简介
!! 没有实用价值，练手的项目，代码写得很糙
一个简单的传感器数据动态展示网站，以Flask为网站框架，Highcharts作前端可视化
使用了MQTT协议订阅传感器实时采集的数据，并结合celery+websocket实现在网页上实时异步刷新（有bug，未能实现通过网页开启celery mqtt订阅任务，需手动从后台开启）

## 安装准备

### MySQL数据库配置
安装好MySQL数据库
安装MySQL-python依赖函数库
建立数据库smartlab (数据库名可任意，稍后需写进项目配置文件中)
新建数据库用户并授予远程连接和全部操作权限
```bash
yum install mysql-server mysql-client
yum install python-devel mysql-devel zlib-devel openssl-devel -y

>create database smartlab
>grant all privileges on smartlab.* to uername@'%' identified by 'yourpassword'
```

### Redis安装配置
安装编译工具
`yum install gcc make`
从官网下载redis源码包
`curl http://download.redis.io/releases/redis-3.0.4.tar.gz -o redis-3.0.4.tar.gz`
解压缩并进入安装目录
`tar zxvf redis-3.0.4.tar.gz &&  cd redis-3.0.4`
编译
`make`
进入源文件的目录
`cd src`
复制 Redis 的服务器和客户端到 /usr/local/bin
`cp redis-server redis-cli /usr/local/bin`
额外配置请参考https://linux.cn/article-6719-1.html


### mosquitto安装配置
从yum源安装mosquitto
```bash
yum install epel-release
yum install mosquitto
```
额外配置请参考https://www.howtoing.com/how-to-install-and-secure-the-mosquitto-mqtt-messaging-broker-on-centos-7/


### python环境配置
安装pip,然后通过pip来安装python虚拟环境工具virtualenv
```bash
easy_install pip
pip install virtualenv
```

### 修改程序配置文件
[db]
DBHOST = localhost
DBNAME = smartlab
DBUSER = root
PASSWORD = 
[mosquitto]
MQTT_HOST = localhost
MQTT_PORT = 1883
MQTT_TOPIC = 
USERNAME = 
PASSWORD = 
[celery_redis]
REDIS_HOST = localhost
REDIS_PORT = 6379
REDIS_DB = 0

### 部署程序
1. 从github上克隆项目到本地
2. 进入项目目录
3. 创建Python虚拟环境
4. 激活虚拟环境
5. 安装配置文件中列出的依赖包
6. 初始化应用数据库
7. 开启web服务
8. 开启celery主程序
  ```bash
  git clone https://github.com/Zhiwei1996/sensor-diagramWEB.git
  cd sensor-diagramWEB
  virtualenv venv
  source venv/bin/activate
  pip install -i https://pypi.douban.com/simple -r requirements.txt
  python manage.py db init
  python manage.py db develop
  gunnicorn --worker--class eventlet -w 1 manage:app -D
  celery -A celery_runner worker --loglevel=info
  ```