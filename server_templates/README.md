# server_templates - 服务器版本模板

## 概述

`server_templates` 文件夹包含服务器版本的模板文件，这些文件用于生成支持点蜡烛功能的Flask服务器版本纪念网页。

## 目录结构

```
server_templates/
├── server_app.py    # Flask服务器应用程序模板
├── template.html    # 服务器版本HTML模板
├── script.js        # 服务器版本JavaScript交互脚本
└── styles.css       # 服务器版本样式文件
```

## 文件说明

### server_app.py

Flask服务器应用程序的主文件，包含：
- 数据库初始化和连接管理
- 点蜡烛API接口
- 静态文件服务
- 主页路由

**主要功能：**
- 初始化SQLite数据库存储蜡烛记录
- 提供RESTful API接口：
  - `GET /api/candles` - 获取所有蜡烛记录
  - `POST /api/candles` - 添加新蜡烛
- 服务静态文件和主页

**配置项：**
- `DATABASE`: SQLite数据库文件路径（默认：candles.db）
- `HOST`: 服务器主机地址（默认：127.0.0.1）
- `PORT`: 服务器端口（默认：5000）

### template.html

服务器版本的HTML模板，包含：
- 基础HTML结构
- 蜡烛显示区域
- 点蜡烛表单
- 纪念内容展示区域

**与静态版本的区别：**
- 包含点蜡烛功能界面
- 使用Flask模板语法（Jinja2）
- 集成了蜡烛API调用

### script.js

服务器版本的JavaScript文件，包含：
- 蜡烛数据获取和显示
- 点蜡烛功能实现
- 页面交互逻辑

**主要函数：**
- `loadCandles()` - 从服务器加载蜡烛数据
- `addCandle(name, message)` - 提交新蜡烛
- `displayCandles(candles)` - 显示蜡烛列表
- `showNotification(message)` - 显示操作提示

### styles.css

服务器版本的样式文件，包含：
- 页面布局样式
- 蜡烛显示样式
- 表单和按钮样式
- 响应式设计

**特色样式：**
- 蜡烛动画效果
- 暗色主题配色
- 流畅的过渡动画

## 使用方法

### 1. 生成服务器版本

通过生成器工具生成服务器版本：
1. 访问生成器网页
2. 填写纪念信息
3. 选择"生成服务器版本"
4. 下载生成的ZIP文件

### 2. 部署服务器

解压生成的ZIP文件后：

```bash
# 安装依赖
pip install flask

# 启动服务器
python server_app.py
```

服务器将在 http://127.0.0.1:5000 启动

### 3. 访问网页

在浏览器中访问服务器地址即可查看纪念网页。

## 自定义配置

### 修改数据库路径

编辑 `server_app.py`：

```python
app.config['DATABASE'] = 'your_database.db'
```

### 修改服务器端口

编辑 `server_app.py`：

```python
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
```

### 自定义样式

编辑 `styles.css` 文件修改页面样式。

## API接口说明

### 获取蜡烛记录

```
GET /api/candles
```

响应示例：
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

### 添加蜡烛

```
POST /api/candles
Content-Type: application/json

{
  "name": "李四",
  "message": "一路走好"
}
```

响应示例：
```json
{
  "success": true,
  "message": "蜡烛已点亮"
}
```

## 注意事项

1. 服务器版本需要Python环境和Flask框架
2. 数据库文件会在首次运行时自动创建
3. 建议在生产环境中使用生产级Web服务器（如Gunicorn、uWSGI）
4. 定期备份数据库文件以防止数据丢失
5. 蜡烛功能不限制用户点击次数，如需限制请修改后端代码

## 故障排除

### 数据库连接错误

确保数据库文件路径正确，且有写入权限。

### 端口被占用

修改 `server_app.py` 中的端口号。

### 蜡烛无法显示

检查浏览器控制台是否有JavaScript错误，确认API接口正常工作。
