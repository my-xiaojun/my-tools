#!/bin/bash
# 一键部署：Python3 + Git + Flask环境 + 放行5000端口

# 1. 更新软件源
sudo yum update -y

# 2. 安装Python3 和 pip
sudo yum install python3 python3-pip -y

# 3. 安装Git
sudo yum install git -y

# 4. 放行防火墙5000端口
sudo firewall-cmd --add-port=5000/tcp --permanent
sudo firewall-cmd --reload

# 5. 安装常用Python依赖
pip3 install flask requests beautifulsoup4

echo "====================================="
echo "✅ 环境全部安装完成"
echo "✅ Python Git Flask 已就绪"
echo "✅ 5000端口已放行"
echo "====================================="