# SmartLabs

## 项目简介
一个简单的传感器数据显示网站，Flask为网站框架，JS做图表显示

1. 用户管理模块，用户分三个等级，三种权限
2. 后台管理模块，admin进入控制台页面，查看敏感传感器数据，查看用户信息
3. 图表显示模块，使用JS扩展库，可视化json数据为多种图表样式，以便友好查看

## 安装准备

### python环境配置
安装pip,然后通过pip来安装python虚拟环境工具virtualenv
```bash
easy_install pip
pip install virtualenv
```

### 部署程序
- 从github上克隆项目到本地
- 进入项目目录
- 创建Python虚拟环境
- 安装MySQL-python依赖函数库
- 激活虚拟环境
- 安装配置文件中列出的依赖包
```bash
git clone https://github.com/Zhiwei1996/SmartLabs
cd SmartLabs
virtualenv venv
yum install python-devel mysql-devel zlib-devel openssl-devel
source venv/bin/activate
pip install -i https://pypi.douban.com/simple -r requirements.txt
```

### 数据库配置
安装好MySQL，建立名为“samrthome”的数据库

### 部署

