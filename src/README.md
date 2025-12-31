# src - 静态版本源文件

## 概述

`src` 文件夹包含静态版本的源文件，这些文件用于生成无需服务器的静态纪念网页。

## 目录结构

```
src/
├── assets/          # 资源文件夹
│   └── README.txt  # 资源说明
├── templates/       # 模板文件
│   ├── script.js   # JavaScript交互脚本
│   └── template.html # HTML模板
└── themes/         # 主题样式
    └── dark.css    # 暗色主题样式
```

## 文件说明

### templates/

#### template.html
- **用途**: 纪念网页的HTML模板
- **功能**: 
  - 页面结构定义
  - 照片展示区域
  - 时间轴显示
  - 点蜡烛按钮（仅展示）
  - 留言板区域（仅展示）
- **特点**: 使用Jinja2模板语法，支持动态内容替换

#### script.js
- **用途**: 前端交互脚本
- **功能**:
  - 照片轮播
  - 音乐播放控制
  - 时间轴动画
  - 点蜡烛动画（仅视觉效果）
- **特点**: 纯前端实现，无需服务器

### themes/

#### dark.css
- **用途**: 页面样式定义
- **功能**:
  - 响应式布局
  - 暗色主题配色
  - 动画效果
  - 移动端适配
- **特点**: 使用CSS3特性，支持现代浏览器

### assets/

#### README.txt
- **用途**: 资源文件夹说明
- **内容**: 指导用户如何放置照片和音乐文件

## 使用方法

### 1. 准备资源文件

在 `assets/` 文件夹中放置：
- 照片文件：`photo1.jpg`, `photo2.jpg`, `photo3.jpg` 等
- 音乐文件：`music.mp3` 或 `music.wav`

### 2. 配置参数

创建配置文件 `config.json`：

```json
{
  "name": "纪念对象名称",
  "dates": "1990 - 2024",
  "subtitle": "副标题",
  "description": "描述信息",
  "themeColor": "#4a9eff",
  "enableCandle": true,
  "enableMessage": false,
  "autoPlayMusic": true,
  "timeline": [
    {
      "year": "2010",
      "event": "大学毕业"
    }
  ]
}
```

### 3. 生成静态页面

使用Node.js生成器：

```bash
cd tools
node generate.js
```

生成的文件将输出到 `output/` 文件夹。

### 4. 查看页面

直接打开 `output/index.html` 即可在浏览器中查看。

## 模板变量

`template.html` 支持以下Jinja2变量：

| 变量名 | 类型 | 说明 |
|--------|------|------|
| name | String | 纪念对象名称 |
| dates | String | 生卒年份 |
| subtitle | String | 副标题 |
| description | String | 描述信息 |
| themeColor | String | 主题颜色（十六进制） |
| enableCandle | Boolean | 是否启用蜡烛功能 |
| enableMessage | Boolean | 是否启用留言功能 |
| autoPlayMusic | Boolean | 是否自动播放音乐 |
| timeline | Array | 时间轴事件数组 |
| photos | Array | 照片文件名数组 |

## 自定义主题

### 修改主题颜色

在 `dark.css` 中修改CSS变量：

```css
:root {
  --primary-color: #4a9eff;
  --text-color: #ffffff;
  --background-color: #1a1a2e;
}
```

### 添加新主题

1. 在 `themes/` 文件夹中创建新的CSS文件，例如 `light.css`
2. 在配置文件中指定主题文件：

```json
{
  "theme": "light.css"
}
```

## 功能限制

由于是静态版本，以下功能仅展示，无法交互：

- ❌ 点蜡烛功能（仅显示按钮，点击无效果）
- ❌ 留言功能（仅显示留言板，无法提交）
- ❌ 数据持久化（所有数据在页面刷新后丢失）

如需完整功能，请使用服务器版本。

## 浏览器兼容性

支持以下浏览器：
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

不支持IE浏览器。

## 性能优化

### 图片优化

建议使用以下工具优化图片：
- TinyPNG: https://tinypng.com/
- ImageOptim: https://imageoptim.com/

### 音乐优化

建议使用以下格式：
- MP3: 128kbps 或 192kbps
- 文件大小: 不超过5MB

## 常见问题

### Q: 照片不显示？
A: 检查照片文件名是否正确，确保照片文件在 `assets/` 文件夹中。

### Q: 音乐无法播放？
A: 确保音乐文件格式正确（MP3或WAV），检查浏览器是否允许自动播放。

### Q: 样式错乱？
A: 确保使用现代浏览器，清除浏览器缓存后重试。

### Q: 如何修改页面布局？
A: 编辑 `template.html` 和 `dark.css` 文件，根据需要调整HTML结构和CSS样式。

## 相关文档

- [项目使用文档](../docs/usage.md)
- [部署文档](../docs/deployment.md)
- [API文档](../docs/api.md)

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本
- 实现基本的静态页面功能
- 支持照片展示、时间轴、音乐播放
