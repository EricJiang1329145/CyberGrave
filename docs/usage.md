# CyberGrave 使用文档

## 项目简介

CyberGrave 是一个快速构建纪念网页的工具，支持两种版本：
- **静态版本**：无需服务器，适合小白用户快速部署
- **服务器版本**：支持点蜡烛功能，需要运行Flask服务器

## 快速开始

### 环境要求

- Python 3.7+
- Node.js 14+ (仅用于静态版本生成)
- 现代浏览器（Chrome、Firefox、Safari、Edge）

### 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Node.js依赖（可选，用于静态版本）
npm install
```

### 启动生成器

```bash
python app.py
```

服务器将在 http://127.0.0.1:5000 启动

## 使用指南

### 1. 访问生成器

在浏览器中打开 http://127.0.0.1:5000

### 2. 填写基本信息

- **纪念对象名称**：必填，例如"张三"
- **生卒年份**：必填，例如"1990 - 2024"
- **副标题**：可选，例如"永远怀念"
- **描述**：可选，描述纪念对象的生平

### 3. 上传照片

- 支持多张照片上传
- 建议使用JPG、PNG格式
- 单张照片不超过10MB
- 总大小不超过50MB

### 4. 添加时间轴

点击"添加时间轴事件"按钮，可以添加多个事件：
- **年份**：例如"2010"
- **事件**：例如"大学毕业"

### 5. 设置主题

- **主题颜色**：选择页面的主色调，默认为蓝色 (#4a9eff)
- 可以使用颜色选择器自定义

### 6. 配置音乐

- 选择音乐文件（MP3、WAV格式）
- 勾选"自动播放音乐"可自动播放背景音乐

### 7. 功能开关

- **启用烛光功能**：显示点蜡烛按钮（静态版本仅展示，服务器版本可交互）
- **启用留言功能**：显示留言板（静态版本仅展示，服务器版本暂未实现）

### 8. 生成页面

#### 生成静态版本

点击"📦 生成静态版本"按钮，生成ZIP文件：
- 解压后直接打开 `index.html` 即可查看
- 可以部署到任何静态网站托管服务（GitHub Pages、Netlify等）
- 无需服务器，适合快速分享

#### 生成服务器版本

点击"🖥️ 生成服务器版本"按钮，生成ZIP文件：
- 包含完整的Flask后端应用
- 支持点蜡烛功能
- 需要运行服务器才能使用

## 部署指南

### 静态版本部署

#### 方式1：直接打开
解压ZIP文件，双击 `index.html` 即可在浏览器中打开

#### 方式2：GitHub Pages
1. 将解压后的文件推送到GitHub仓库
2. 在仓库设置中启用GitHub Pages
3. 选择主分支作为源
4. 访问生成的URL

#### 方式3：Netlify
1. 访问 https://www.netlify.com/
2. 拖拽解压后的文件夹到上传区域
3. 等待部署完成
4. 获得可访问的URL

### 服务器版本部署

#### 本地运行
```bash
# 解压ZIP文件
cd 解压后的文件夹

# 安装依赖
pip install -r requirements.txt

# 运行服务器
python app.py
```

访问 http://127.0.0.1:5000

#### 服务器部署
```bash
# 使用Gunicorn（推荐）
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 或使用uWSGI
pip install uwsgi
uwsgi --http :5000 --wsgi-file app.py --callable app
```

#### Docker部署（可选）
创建 `Dockerfile`：
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

构建和运行：
```bash
docker build -t cyber-grave .
docker run -p 5000:5000 cyber-grave
```

## 功能说明

### 静态版本功能
- ✅ 照片展示
- ✅ 人生时间轴
- ✅ 背景音乐播放
- ✅ 响应式设计
- ✅ 暗色主题
- ❌ 点蜡烛（仅展示）
- ❌ 留言功能（仅展示）

### 服务器版本功能
- ✅ 照片展示
- ✅ 人生时间轴
- ✅ 背景音乐播放
- ✅ 响应式设计
- ✅ 暗色主题
- ✅ 点蜡烛功能（支持自定义姓名和留言）
- ✅ 实时显示蜡烛总数
- ✅ 显示所有点蜡烛记录
- ❌ 留言功能（暂未实现）

## 点蜡烛功能（服务器版本）

### 功能特点
- 用户可以输入姓名（可选，默认为"匿名"）
- 可以添加留言（可选）
- 不限制点蜡烛次数
- 实时显示蜡烛总数
- 显示所有点蜡烛记录（姓名、留言、时间）
- 点蜡烛时有动画效果

### 数据存储
- 使用SQLite数据库存储蜡烛数据
- 数据库文件：`candles.db`
- 自动创建，无需手动配置

### API接口

#### 获取所有蜡烛记录
```
GET /api/candles
```

返回示例：
```json
[
  {
    "id": 1,
    "name": "张三",
    "message": "永远怀念",
    "created_at": "2024-01-01 12:00:00"
  }
]
```

#### 点蜡烛
```
POST /api/candles
Content-Type: application/json

{
  "name": "张三",
  "message": "永远怀念"
}
```

返回示例：
```json
{
  "success": true,
  "message": "蜡烛已点亮"
}
```

#### 获取蜡烛总数
```
GET /api/candles/count
```

返回示例：
```json
{
  "count": 10
}
```

## 常见问题

### Q: 静态版本和服务器版本有什么区别？
A: 静态版本无需服务器，可以直接打开HTML文件，但点蜡烛和留言功能仅展示；服务器版本需要运行Flask服务器，支持完整的点蜡烛交互功能。

### Q: 如何备份服务器版本的数据？
A: 备份 `candles.db` 文件即可。建议定期备份数据库文件。

### Q: 可以自定义主题颜色吗？
A: 可以，在生成器中使用颜色选择器选择您喜欢的颜色。

### Q: 照片和音乐文件有大小限制吗？
A: 单个文件不超过10MB，总大小不超过50MB。

### Q: 服务器版本可以在生产环境使用吗？
A: 可以，但建议使用专业的WSGI服务器（如Gunicorn、uWSGI）而不是Flask的开发服务器。

### Q: 如何修改服务器版本的端口？
A: 编辑 `app.py` 文件，修改最后一行的 `port=5000` 为您想要的端口号。

## 技术栈

### 前端
- HTML5
- CSS3（响应式设计）
- JavaScript（ES6+）
- Fetch API

### 后端（服务器版本）
- Python 3.7+
- Flask 3.0.0
- SQLite

### 工具
- Node.js（静态版本生成）
- npm

## 项目结构

```
CyberGrave/
├── app.py                    # Flask生成器应用
├── requirements.txt          # Python依赖
├── package.json             # Node.js配置
├── docs/                    # 文档目录
│   ├── usage.md             # 使用文档（本文件）
│   ├── deployment.md        # 部署文档
│   └── api.md               # API文档
├── src/                     # 静态版本源文件
├── server_templates/        # 服务器版本模板
├── templates/               # 生成器模板
├── static/                  # 生成器静态资源
└── tools/                   # 工具脚本
```

## 许可证

本项目仅供学习和个人使用。

## 联系方式

如有问题或建议，欢迎提交Issue。
