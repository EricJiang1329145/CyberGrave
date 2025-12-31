# CyberGrave API 文档

## 概述

CyberGrave 服务器版本提供RESTful API接口，主要用于点蜡烛功能。

## 基础信息

- **Base URL**: `http://your-domain.com` 或 `http://127.0.0.1:5000`
- **数据格式**: JSON
- **字符编码**: UTF-8

## API 接口

### 1. 获取所有蜡烛记录

获取系统中所有蜡烛记录，按创建时间倒序排列。

**请求**
```
GET /api/candles
```

**参数**
无

**响应示例**
```json
[
  {
    "id": 1,
    "name": "张三",
    "message": "永远怀念",
    "created_at": "2024-01-01 12:00:00"
  },
  {
    "id": 2,
    "name": "李四",
    "message": "一路走好",
    "created_at": "2024-01-01 13:30:00"
  }
]
```

**响应字段说明**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 蜡烛ID，自增主键 |
| name | String | 点蜡烛人的姓名 |
| message | String | 留言内容 |
| created_at | String | 创建时间，格式：YYYY-MM-DD HH:MM:SS |

**状态码**
- `200 OK`: 成功获取蜡烛列表

**示例代码**
```javascript
// JavaScript Fetch API
fetch('/api/candles')
  .then(response => response.json())
  .then(data => {
    console.log(data);
    // 处理蜡烛数据
  })
  .catch(error => {
    console.error('获取蜡烛失败:', error);
  });
```

```python
# Python requests
import requests

response = requests.get('http://127.0.0.1:5000/api/candles')
candles = response.json()
print(candles)
```

```bash
# cURL
curl http://127.0.0.1:5000/api/candles
```

---

### 2. 点蜡烛

添加一个新的蜡烛记录。

**请求**
```
POST /api/candles
```

**请求头**
```
Content-Type: application/json
```

**请求体**
```json
{
  "name": "张三",
  "message": "永远怀念"
}
```

**请求参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | String | 否 | 点蜡烛人的姓名，默认为"匿名" |
| message | String | 否 | 留言内容，默认为空字符串 |

**响应示例**
```json
{
  "success": true,
  "message": "蜡烛已点亮"
}
```

**响应字段说明**
| 字段 | 类型 | 说明 |
|------|------|------|
| success | Boolean | 操作是否成功 |
| message | String | 返回消息 |

**状态码**
- `201 Created`: 成功添加蜡烛
- `400 Bad Request`: 请求参数错误
- `500 Internal Server Error`: 服务器内部错误

**示例代码**
```javascript
// JavaScript Fetch API
fetch('/api/candles', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: '张三',
    message: '永远怀念'
  })
})
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log(data.message);
      // 刷新蜡烛列表
      loadCandles();
    }
  })
  .catch(error => {
    console.error('点蜡烛失败:', error);
  });
```

```python
# Python requests
import requests

data = {
  'name': '张三',
  'message': '永远怀念'
}

response = requests.post(
  'http://127.0.0.1:5000/api/candles',
  json=data
)

result = response.json()
print(result)
```

```bash
# cURL
curl -X POST http://127.0.0.1:5000/api/candles \
  -H "Content-Type: application/json" \
  -d '{"name":"张三","message":"永远怀念"}'
```

---

### 3. 获取蜡烛总数

获取系统中所有蜡烛的总数。

**请求**
```
GET /api/candles/count
```

**参数**
无

**响应示例**
```json
{
  "count": 10
}
```

**响应字段说明**
| 字段 | 类型 | 说明 |
|------|------|------|
| count | Integer | 蜡烛总数 |

**状态码**
- `200 OK`: 成功获取蜡烛总数

**示例代码**
```javascript
// JavaScript Fetch API
fetch('/api/candles/count')
  .then(response => response.json())
  .then(data => {
    console.log('蜡烛总数:', data.count);
    // 更新UI显示
    document.getElementById('candle-count').textContent = data.count;
  })
  .catch(error => {
    console.error('获取蜡烛总数失败:', error);
  });
```

```python
# Python requests
import requests

response = requests.get('http://127.0.0.1:5000/api/candles/count')
result = response.json()
print('蜡烛总数:', result['count'])
```

```bash
# cURL
curl http://127.0.0.1:5000/api/candles/count
```

---

## 错误处理

### 错误响应格式

所有错误响应都遵循统一格式：

```json
{
  "error": "错误描述信息"
}
```

### 常见错误

| 状态码 | 错误类型 | 说明 |
|--------|----------|------|
| 400 | Bad Request | 请求参数错误 |
| 404 | Not Found | 资源不存在 |
| 500 | Internal Server Error | 服务器内部错误 |

### 错误示例

**请求参数错误**
```json
{
  "error": "无效的请求参数"
}
```

**服务器内部错误**
```json
{
  "error": "数据库连接失败"
}
```

---

## 使用示例

### 完整的点蜡烛流程

```javascript
// 1. 获取当前蜡烛总数
async function getCandleCount() {
  const response = await fetch('/api/candles/count');
  const data = await response.json();
  return data.count;
}

// 2. 点蜡烛
async function lightCandle(name, message) {
  const response = await fetch('/api/candles', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: name || '匿名',
      message: message || ''
    })
  });
  
  const data = await response.json();
  return data;
}

// 3. 获取所有蜡烛记录
async function getAllCandles() {
  const response = await fetch('/api/candles');
  const data = await response.json();
  return data;
}

// 4. 完整流程
async function completeFlow() {
  try {
    // 获取当前总数
    const count = await getCandleCount();
    console.log('当前蜡烛数:', count);
    
    // 点蜡烛
    const result = await lightCandle('张三', '永远怀念');
    console.log(result.message);
    
    // 获取新的总数
    const newCount = await getCandleCount();
    console.log('新的蜡烛数:', newCount);
    
    // 获取所有蜡烛记录
    const candles = await getAllCandles();
    console.log('所有蜡烛:', candles);
    
  } catch (error) {
    console.error('操作失败:', error);
  }
}

// 执行流程
completeFlow();
```

---

## 数据库结构

### candles 表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 蜡烛ID |
| name | TEXT | NOT NULL | 点蜡烛人的姓名 |
| message | TEXT | - | 留言内容 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

### SQL创建语句

```sql
CREATE TABLE IF NOT EXISTS candles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

## 限制和注意事项

### 请求限制
- 无需认证即可访问
- 不限制点蜡烛次数
- 不限制每个用户的点蜡烛次数

### 数据存储
- 使用SQLite数据库
- 数据库文件：`candles.db`
- 建议定期备份数据库

### 性能考虑
- 蜡烛记录数量无硬性限制
- 建议定期清理旧数据
- 大量数据时考虑分页查询

### 安全建议
- 生产环境建议添加认证机制
- 限制请求频率防止滥用
- 定期备份数据库
- 使用HTTPS保护数据传输

---

## 未来扩展

### 计划中的功能

1. **用户认证**
   - 支持用户注册和登录
   - 限制匿名用户点蜡烛次数

2. **分页查询**
   - 支持分页获取蜡烛记录
   - 添加排序和筛选功能

3. **数据统计**
   - 按日期统计点蜡烛数量
   - 按用户统计点蜡烛次数

4. **导出功能**
   - 导出蜡烛记录为CSV
   - 导出蜡烛记录为JSON

5. **管理接口**
   - 删除不当留言
   - 封禁恶意用户

---

## 版本历史

### v1.0.0 (2024-01-01)
- 初始版本
- 实现基本的点蜡烛功能
- 提供三个API接口

---

## 技术支持

如有问题或建议，请提交Issue或联系开发团队。
