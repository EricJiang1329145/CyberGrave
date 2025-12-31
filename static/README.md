# static - 生成器静态资源

## 概述

`static` 文件夹包含CyberGrave生成器的静态资源文件，主要是CSS样式文件。

## 目录结构

```
static/
└── generator.css    # 生成器页面样式
```

## 文件说明

### generator.css

生成器页面的主样式文件，定义了整个生成器界面的视觉风格。

**样式特点：**
- 现代化设计风格
- 响应式布局
- 暗色主题配色
- 流畅的动画效果
- 移动端适配

**主要样式模块：**

#### 1. 全局样式

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #1a1a2e;
  color: #eee;
}
```

#### 2. 布局容器

```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  padding: 40px 0;
}
```

#### 3. 表单样式

```css
.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #16213e;
  color: #eee;
}
```

#### 4. 按钮样式

```css
.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #e94560;
  color: white;
}

.btn-primary:hover {
  background-color: #ff6b6b;
}
```

#### 5. 预览区域

```css
.preview-container {
  border: 2px solid #444;
  border-radius: 8px;
  padding: 20px;
  margin-top: 30px;
  background-color: #0f3460;
}
```

#### 6. 响应式设计

```css
@media (max-width: 768px) {
  .container {
    padding: 10px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}
```

## 颜色方案

生成器使用暗色主题，主要颜色包括：

- **背景色**：
  - 主背景：`#1a1a2e`
  - 次背景：`#16213e`
  - 卡片背景：`#0f3460`

- **文字色**：
  - 主文字：`#eee`
  - 次文字：`#ccc`
  - 强调文字：`#e94560`

- **强调色**：
  - 主按钮：`#e94560`
  - 悬停状态：`#ff6b6b`
  - 边框：`#444`

## 自定义样式

### 修改颜色主题

编辑 `generator.css` 中的颜色变量：

```css
:root {
  --primary-color: #e94560;
  --background-color: #1a1a2e;
  --text-color: #eee;
}
```

### 调整布局

修改容器宽度和间距：

```css
.container {
  max-width: 1400px;  /* 调整最大宽度 */
  padding: 30px;      /* 调整内边距 */
}
```

### 修改字体

更改全局字体设置：

```css
body {
  font-family: 'Your Font', sans-serif;
  font-size: 16px;
  line-height: 1.6;
}
```

## 动画效果

样式文件包含多种动画效果：

### 按钮悬停动画

```css
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(233, 69, 96, 0.4);
}
```

### 输入框聚焦动画

```css
.form-input:focus {
  outline: none;
  border-color: #e94560;
  box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.1);
}
```

### 页面加载动画

```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

## 响应式断点

样式文件使用以下响应式断点：

- **桌面端**：> 768px
- **移动端**：≤ 768px

```css
@media (max-width: 768px) {
  /* 移动端样式 */
}
```

## 浏览器兼容性

样式文件支持以下浏览器：

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

使用的CSS特性：
- Flexbox布局
- Grid布局
- CSS变量
- CSS动画
- 媒体查询

## 性能优化

样式文件已进行以下优化：

1. **CSS压缩**：生产环境建议压缩CSS文件
2. **选择器优化**：避免过深的嵌套选择器
3. **动画优化**：使用transform和opacity进行动画
4. **响应式图片**：配合HTML的srcset属性

## 使用方法

### 在HTML中引入

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="{{ url_for('static', filename='generator.css') }}">
</head>
<body>
  <!-- 页面内容 -->
</body>
</html>
```

### 在Flask模板中使用

```html
<link rel="stylesheet" href="{{ url_for('static', filename='generator.css') }}">
```

## 注意事项

1. 样式文件使用相对路径引用
2. 确保静态文件路由配置正确
3. 修改样式后需要清除浏览器缓存
4. 建议使用CSS预处理器（如Sass）进行复杂样式开发
5. 生产环境建议压缩CSS文件以减小文件大小

## 扩展开发

### 添加新的样式组件

在 `generator.css` 中添加新的样式类：

```css
.new-component {
  /* 样式定义 */
}
```

### 创建主题变体

创建新的主题文件：

```css
/* generator-light.css */
:root {
  --primary-color: #007bff;
  --background-color: #ffffff;
  --text-color: #333333;
}
```

### 添加动画效果

定义新的关键帧动画：

```css
@keyframes newAnimation {
  from {
    /* 起始状态 */
  }
  to {
    /* 结束状态 */
  }
}
```
