# CyberGrave 部署文档

## 部署概述

CyberGrave 提供两种部署方式：
1. **静态版本部署**：无需服务器，适合快速分享
2. **服务器版本部署**：需要运行Flask服务器，支持点蜡烛功能

## 静态版本部署

### 方式1：本地直接打开

最简单的方式，适合个人使用或小范围分享。

**步骤：**
1. 使用生成器生成静态版本ZIP文件
2. 解压ZIP文件
3. 双击 `index.html` 在浏览器中打开

**优点：**
- 无需任何服务器
- 零配置
- 适合离线查看

**缺点：**
- 无法使用点蜡烛功能
- 不方便在线分享

### 方式2：GitHub Pages

适合开源项目或免费托管。

**步骤：**

1. **创建GitHub仓库**
   - 登录GitHub，创建新仓库
   - 仓库名称可以是任意名称

2. **上传文件**
   ```bash
   # 解压ZIP文件
   unzip cyber_grave_20240101_120000.zip -d cyber-grave
   cd cyber-grave
   
   # 初始化Git仓库
   git init
   git add .
   git commit -m "Initial commit"
   
   # 添加远程仓库
   git remote add origin https://github.com/your-username/your-repo.git
   
   # 推送到GitHub
   git branch -M main
   git push -u origin main
   ```

3. **启用GitHub Pages**
   - 进入仓库设置（Settings）
   - 找到"Pages"选项
   - 在"Source"中选择"Deploy from a branch"
   - 选择"main"分支和"/ (root)"目录
   - 点击"Save"

4. **访问网站**
   - 等待几分钟，GitHub会自动部署
   - 访问 `https://your-username.github.io/your-repo/`

**优点：**
- 完全免费
- 自动HTTPS
- 支持自定义域名
- 版本控制

**缺点：**
- 仅支持静态内容
- 无法使用点蜡烛功能

### 方式3：Netlify

最简单的部署方式，支持拖拽上传。

**步骤：**

1. **注册Netlify账户**
   - 访问 https://www.netlify.com/
   - 注册账户（免费）

2. **拖拽上传**
   - 解压ZIP文件
   - 登录Netlify
   - 将解压后的文件夹拖拽到上传区域
   - 等待部署完成

3. **访问网站**
   - Netlify会自动生成一个URL
   - 可以在设置中修改域名

**优点：**
- 部署极快
- 支持拖拽上传
- 自动HTTPS
- 支持自定义域名
- 免费额度充足

**缺点：**
- 仅支持静态内容
- 无法使用点蜡烛功能

### 方式4：Vercel

类似Netlify，专注于前端部署。

**步骤：**

1. **注册Vercel账户**
   - 访问 https://vercel.com/
   - 注册账户（免费）

2. **导入项目**
   - 将文件推送到GitHub
   - 在Vercel中导入GitHub仓库
   - 选择"Other"作为预设
   - 点击"Deploy"

3. **访问网站**
   - Vercel会自动生成URL
   - 可以在设置中修改域名

**优点：**
- 部署速度快
- 自动HTTPS
- 支持自定义域名
- 免费额度充足

**缺点：**
- 仅支持静态内容
- 无法使用点蜡烛功能

## 服务器版本部署

### 方式1：本地运行

适合开发和测试。

**步骤：**

1. **生成服务器版本**
   - 使用生成器生成服务器版本ZIP文件
   - 下载并解压

2. **安装依赖**
   ```bash
   cd 解压后的文件夹
   pip install -r requirements.txt
   ```

3. **运行服务器**
   ```bash
   python app.py
   ```

4. **访问网站**
   - 打开浏览器访问 http://127.0.0.1:5000

**优点：**
- 完全控制
- 支持点蜡烛功能
- 适合本地测试

**缺点：**
- 仅限本地访问
- 不适合生产环境

### 方式2：云服务器部署

适合生产环境，支持公网访问。

#### 使用Gunicorn（推荐）

**步骤：**

1. **购买云服务器**
   - 阿里云、腾讯云、AWS等
   - 选择Ubuntu 20.04或CentOS 7+

2. **安装Python环境**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   
   # CentOS/RHEL
   sudo yum install python3 python3-pip
   ```

3. **创建虚拟环境**
   ```bash
   mkdir ~/cyber-grave
   cd ~/cyber-grave
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **上传文件**
   ```bash
   # 使用scp上传
   scp -r 本地文件夹/* user@server-ip:~/cyber-grave/
   
   # 或使用rsync
   rsync -avz 本地文件夹/ user@server-ip:~/cyber-grave/
   ```

5. **安装依赖**
   ```bash
   pip install -r requirements.txt
   pip install gunicorn
   ```

6. **运行Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

7. **配置防火墙**
   ```bash
   # Ubuntu/Debian
   sudo ufw allow 5000
   
   # CentOS/RHEL
   sudo firewall-cmd --permanent --add-port=5000/tcp
   sudo firewall-cmd --reload
   ```

8. **访问网站**
   - 打开浏览器访问 http://your-server-ip:5000

**使用Systemd管理服务**

创建服务文件：
```bash
sudo nano /etc/systemd/system/cyber-grave.service
```

内容：
```ini
[Unit]
Description=CyberGrave Flask Application
After=network.target

[Service]
User=your-username
Group=www-data
WorkingDirectory=/home/your-username/cyber-grave
Environment="PATH=/home/your-username/cyber-grave/venv/bin"
ExecStart=/home/your-username/cyber-grave/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable cyber-grave
sudo systemctl start cyber-grave
sudo systemctl status cyber-grave
```

#### 使用uWSGI

**安装uWSGI：**
```bash
pip install uwsgi
```

**创建配置文件：**
```bash
nano uwsgi.ini
```

内容：
```ini
[uwsgi]
module = app:app
master = true
processes = 4
socket = 0.0.0.0:5000
chmod-socket = 660
vacuum = true
die-on-term = true
```

**运行uWSGI：**
```bash
uwsgi --ini uwsgi.ini
```

### 方式3：Docker部署

适合容器化部署，易于管理和扩展。

**步骤：**

1. **创建Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

2. **构建镜像**
   ```bash
   docker build -t cyber-grave .
   ```

3. **运行容器**
   ```bash
   docker run -d \
     --name cyber-grave \
     -p 5000:5000 \
     -v $(pwd)/candles.db:/app/candles.db \
     cyber-grave
   ```

4. **访问网站**
   - 打开浏览器访问 http://localhost:5000

**使用Docker Compose（推荐）**

创建 `docker-compose.yml`：
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./candles.db:/app/candles.db
    restart: unless-stopped
```

运行：
```bash
docker-compose up -d
```

### 方式4：Nginx反向代理

适合生产环境，支持HTTPS和域名访问。

**步骤：**

1. **安装Nginx**
   ```bash
   # Ubuntu/Debian
   sudo apt install nginx
   
   # CentOS/RHEL
   sudo yum install nginx
   ```

2. **配置Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/cyber-grave
   ```

内容：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. **启用配置**
   ```bash
   sudo ln -s /etc/nginx/sites-available/cyber-grave /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

4. **配置HTTPS（使用Let's Encrypt）**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

### 方式5：云平台部署

#### Heroku

1. **安装Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **登录Heroku**
   ```bash
   heroku login
   ```

3. **创建应用**
   ```bash
   heroku create your-app-name
   ```

4. **部署**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   heroku git:remote -a your-app-name
   git push heroku main
   ```

5. **访问网站**
   - 访问 https://your-app-name.herokuapp.com

#### 阿里云函数计算

1. **创建函数**
   - 登录阿里云控制台
   - 进入函数计算服务
   - 创建新函数

2. **上传代码**
   - 选择"自定义运行时"
   - 上传ZIP文件

3. **配置环境**
   - 设置入口为 `app.app`
   - 配置内存和超时时间

4. **访问网站**
   - 获取函数的访问URL

## 数据备份

### SQLite数据库备份

**手动备份：**
```bash
# 备份
cp candles.db candles.db.backup.$(date +%Y%m%d)

# 恢复
cp candles.db.backup.20240101 candles.db
```

**自动备份脚本：**
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

cp candles.db $BACKUP_DIR/candles.db.$DATE

# 保留最近7天的备份
find $BACKUP_DIR -name "candles.db.*" -mtime +7 -delete
```

添加到crontab：
```bash
crontab -e
# 每天凌晨2点备份
0 2 * * * /path/to/backup.sh
```

## 性能优化

### Gunicorn配置优化

```bash
# 根据CPU核心数调整worker数量
gunicorn -w $(nproc) -b 0.0.0.0:5000 app:app

# 使用gevent worker（高并发）
pip install gevent
gunicorn -k gevent -w 4 -b 0.0.0.0:5000 app:app
```

### Nginx缓存配置

```nginx
proxy_cache_path /path/to/cache levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

server {
    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 60m;
        proxy_pass http://127.0.0.1:5000;
    }
}
```

## 监控和日志

### 查看日志

```bash
# Systemd服务日志
sudo journalctl -u cyber-grave -f

# Gunicorn日志
tail -f /var/log/gunicorn/error.log

# Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 使用Sentry监控错误

1. 注册Sentry账户
2. 安装SDK：
   ```bash
   pip install sentry-sdk
   ```

3. 在app.py中添加：
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.flask import FlaskIntegration
   
   sentry_sdk.init(
       dsn="your-sentry-dsn",
       integrations=[FlaskIntegration()],
       traces_sample_rate=1.0
   )
   ```

## 安全建议

1. **使用HTTPS**
   - 配置SSL证书
   - 强制HTTPS重定向

2. **限制访问**
   - 配置防火墙规则
   - 使用fail2ban防止暴力破解

3. **定期更新**
   - 更新Python依赖
   - 更新系统补丁

4. **备份数据**
   - 定期备份数据库
   - 测试恢复流程

## 故障排查

### 常见问题

**Q: 端口被占用**
```bash
# 查找占用端口的进程
lsof -i :5000
# 或
netstat -tlnp | grep 5000

# 杀死进程
kill -9 PID
```

**Q: 权限问题**
```bash
# 修改文件权限
chmod 644 app.py
chmod 755 templates/
```

**Q: 数据库锁定**
```bash
# 删除数据库锁文件
rm -f candles.db-wal candles.db-shm
```

**Q: 内存不足**
```bash
# 减少worker数量
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

## 总结

选择合适的部署方式：
- **快速分享**：使用静态版本 + GitHub Pages/Netlify
- **个人使用**：本地运行服务器版本
- **生产环境**：云服务器 + Gunicorn + Nginx
- **容器化**：Docker + Docker Compose
- **云平台**：Heroku、阿里云函数计算等
