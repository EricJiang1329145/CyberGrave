# templates - 生成器前端模板

## 概述

`templates` 文件夹包含CyberGrave生成器的前端模板文件，用于构建用户友好的网页生成界面。

## 目录结构

```
templates/
├── generator.html    # 主生成器页面
└── preview.html      # 预览页面
```

## 文件说明

### generator.html

主生成器页面，提供完整的表单界面用于配置纪念网页。

**主要功能：**
- 纪念信息输入（姓名、生平简介、纪念词等）
- 照片上传
- 音乐选择
- 主题配置
- 版本选择（静态/服务器）
- 实时预览
- 文件生成和下载

**表单字段：**
- **基本信息**
  - 姓名
  - 生卒日期
  - 生平简介
  - 纪念词

- **媒体资源**
  - 照片上传（支持多张）
  - 音乐选择（内置或自定义）

- **样式配置**
  - 主题选择（暗色/亮色）
  - 字体大小
  - 颜色方案

- **生成选项**
  - 版本类型（静态/服务器）
  - 生成按钮

**JavaScript功能：**
- 表单验证
- 文件上传处理
- 实时预览更新
- 生成请求发送
- 下载文件处理

### preview.html

预览页面，用于在生成前查看纪念网页的效果。

**主要功能：**
- 显示预览内容
- 响应式布局
- 与实际生成页面保持一致

**使用方式：**
通过生成器的"预览"按钮打开，显示当前配置的纪念网页效果。

## 技术栈

- **HTML5**: 页面结构
- **CSS3**: 样式和布局
- **JavaScript**: 交互逻辑
- **Fetch API**: 与后端通信
- **Flask模板引擎**: 服务端渲染（如果需要）

## 主要功能模块

### 1. 表单处理

```javascript
// 表单提交
document.getElementById('generateForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  // 处理表单数据
});
```

### 2. 文件上传

支持照片和音乐文件上传：
- 照片：JPG、PNG格式
- 音乐：MP3格式
- 文件大小限制：10MB

### 3. 预览功能

```javascript
// 打开预览
async function openPreview() {
  const config = getFormConfig();
  const response = await fetch('/preview', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(config)
  });
  // 处理预览响应
}
```

### 4. 生成功能

```javascript
// 生成网页
async function generatePage(version) {
  const config = getFormConfig();
  const response = await fetch('/generate_' + version, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(config)
  });
  // 下载生成的文件
}
```

## 样式说明

生成器页面使用独立的样式文件 `static/generator.css`，包含：
- 响应式布局
- 现代化UI设计
- 表单样式
- 按钮和交互效果
- 移动端适配

## 自定义开发

### 添加新的表单字段

1. 在 `generator.html` 中添加HTML元素
2. 在JavaScript中添加字段处理逻辑
3. 更新配置对象结构

### 添加新的主题选项

1. 在表单中添加主题选择器
2. 在生成逻辑中处理主题参数
3. 在模板中应用主题样式

### 修改预览逻辑

编辑 `preview.html` 和相关JavaScript代码以调整预览行为。

## API接口

### /preview

预览接口，返回预览HTML。

**请求：**
```json
POST /preview
Content-Type: application/json

{
  "name": "姓名",
  "birth_date": "1950-01-01",
  "death_date": "2024-01-01",
  // ...其他配置
}
```

**响应：**
```html
<!DOCTYPE html>
<!-- 预览HTML内容 -->
```

### /generate_static

生成静态版本接口。

**请求：**
```json
POST /generate_static
Content-Type: application/json

{
  // 配置对象
}
```

**响应：**
- Content-Type: application/zip
- ZIP文件包含生成的静态网页

### /generate_server

生成服务器版本接口。

**请求：**
```json
POST /generate_server
Content-Type: application/json

{
  // 配置对象
}
```

**响应：**
- Content-Type: application/zip
- ZIP文件包含服务器版本文件

## 浏览器兼容性

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 注意事项

1. 文件上传有大小限制（默认10MB）
2. 预览功能需要JavaScript支持
3. 生成过程可能需要几秒钟，请耐心等待
4. 建议使用现代浏览器以获得最佳体验
5. 生成的大文件可能需要较长时间下载

## 故障排除

### 预览无法显示

- 检查浏览器控制台是否有错误
- 确认后端服务正常运行
- 检查网络连接

### 生成失败

- 检查表单数据是否完整
- 查看后端日志获取错误信息
- 确认文件上传未超时

### 下载失败

- 检查浏览器下载设置
- 确认有足够的磁盘空间
- 尝试使用不同的浏览器
