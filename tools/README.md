# tools - 工具脚本

## 概述

`tools` 文件夹包含CyberGrave项目的工具脚本，主要用于生成静态版本的纪念网页。

## 目录结构

```
tools/
└── generate.js    # Node.js页面生成工具
```

## 文件说明

### generate.js

Node.js脚本，用于从配置文件生成静态纪念网页。

**主要功能：**
- 读取JSON配置文件
- 处理HTML模板
- 替换模板变量
- 生成静态HTML文件
- 复制资源文件到输出目录

**使用方法：**

```bash
node tools/generate.js [配置文件路径]
```

**参数说明：**
- `配置文件路径`：JSON配置文件的路径（可选，默认为 `config.json`）

**示例：**

```bash
# 使用默认配置
node tools/generate.js

# 使用指定配置
node tools/generate.js my_config.json
```

## 配置文件格式

配置文件使用JSON格式，包含以下字段：

```json
{
  "name": "姓名",
  "birth_date": "1950-01-01",
  "death_date": "2024-01-01",
  "biography": "生平简介",
  "tribute": "纪念词",
  "photos": ["photo1.jpg", "photo2.jpg"],
  "music": "music.mp3",
  "theme": "dark"
}
```

**字段说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 纪念者姓名 |
| birth_date | string | 是 | 出生日期（YYYY-MM-DD） |
| death_date | string | 是 | 去世日期（YYYY-MM-DD） |
| biography | string | 是 | 生平简介 |
| tribute | string | 是 | 纪念词 |
| photos | array | 否 | 照片文件名列表 |
| music | string | 否 | 音乐文件名 |
| theme | string | 否 | 主题名称（dark/light） |

## 工作流程

### 1. 读取配置

```javascript
const config = require(configPath);
```

### 2. 读取模板

```javascript
const fs = require('fs');
const template = fs.readFileSync('src/templates/template.html', 'utf-8');
```

### 3. 替换变量

```javascript
let html = template
  .replace('{{name}}', config.name)
  .replace('{{birth_date}}', config.birth_date)
  .replace('{{death_date}}', config.death_date)
  // ... 其他替换
```

### 4. 生成输出文件

```javascript
fs.writeFileSync(outputPath, html);
```

### 5. 复制资源文件

```javascript
// 复制CSS
fs.copyFileSync('src/themes/dark.css', 'output/dark.css');

// 复制JavaScript
fs.copyFileSync('src/templates/script.js', 'output/script.js');

// 复制照片和音乐
config.photos.forEach(photo => {
  fs.copyFileSync(`assets/${photo}`, `output/${photo}`);
});
```

## 输出结构

生成的静态网页包含以下文件：

```
output/
├── index.html      # 主页面
├── dark.css        # 样式文件
├── script.js       # JavaScript文件
├── photo1.jpg      # 照片文件
├── photo2.jpg      # 照片文件
└── music.mp3       # 音乐文件
```

## 依赖项

### Node.js模块

- `fs`：文件系统操作（内置）
- `path`：路径处理（内置）

无需安装额外的npm包。

## 环境要求

- Node.js 14.0.0 或更高版本

## 命令行选项

### 基本用法

```bash
node tools/generate.js [options]
```

### 选项

| 选项 | 说明 |
|------|------|
| `-h, --help` | 显示帮助信息 |
| `-v, --version` | 显示版本信息 |
| `-c, --config <path>` | 指定配置文件路径 |
| `-o, --output <path>` | 指定输出目录 |

### 示例

```bash
# 显示帮助
node tools/generate.js --help

# 使用自定义配置文件
node tools/generate.js --config my_config.json

# 指定输出目录
node tools/generate.js --output my_output
```

## 错误处理

脚本包含以下错误处理：

### 1. 配置文件不存在

```javascript
if (!fs.existsSync(configPath)) {
  console.error('错误：配置文件不存在');
  process.exit(1);
}
```

### 2. 模板文件不存在

```javascript
if (!fs.existsSync(templatePath)) {
  console.error('错误：模板文件不存在');
  process.exit(1);
}
```

### 3. 资源文件缺失

```javascript
config.photos.forEach(photo => {
  const photoPath = `assets/${photo}`;
  if (!fs.existsSync(photoPath)) {
    console.warn(`警告：照片文件不存在 - ${photo}`);
  }
});
```

## 自定义开发

### 添加新的配置字段

1. 在配置文件格式中添加新字段
2. 在 `generate.js` 中添加替换逻辑
3. 在模板文件中添加对应的占位符

### 修改模板路径

```javascript
const templatePath = 'path/to/your/template.html';
```

### 修改输出目录

```javascript
const outputDir = 'path/to/output';
```

### 添加预处理逻辑

在替换变量之前添加自定义处理：

```javascript
// 示例：格式化日期
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN');
}

const formattedDate = formatDate(config.birth_date);
html = html.replace('{{birth_date}}', formattedDate);
```

## 性能优化

### 1. 批量文件操作

使用Promise.all进行并行文件操作：

```javascript
const copyPromises = config.photos.map(photo => {
  return copyFile(`assets/${photo}`, `output/${photo}`);
});
await Promise.all(copyPromises);
```

### 2. 缓存模板

对于多次生成，可以缓存模板内容：

```javascript
let cachedTemplate = null;

function getTemplate() {
  if (!cachedTemplate) {
    cachedTemplate = fs.readFileSync(templatePath, 'utf-8');
  }
  return cachedTemplate;
}
```

## 测试

### 测试配置文件

创建测试配置文件 `test_config.json`：

```json
{
  "name": "测试用户",
  "birth_date": "1990-01-01",
  "death_date": "2024-01-01",
  "biography": "这是测试简介",
  "tribute": "这是测试纪念词",
  "photos": [],
  "music": "",
  "theme": "dark"
}
```

运行测试：

```bash
node tools/generate.js test_config.json
```

### 验证输出

检查生成的 `output/index.html` 文件是否正确。

## 故障排除

### 问题：Node.js版本过低

**解决方案：**
```bash
# 检查Node.js版本
node --version

# 升级Node.js
# 访问 https://nodejs.org 下载最新版本
```

### 问题：配置文件格式错误

**解决方案：**
使用JSON验证工具检查配置文件格式：
```bash
node -e "console.log(JSON.stringify(JSON.parse(require('fs').readFileSync('config.json'))))"
```

### 问题：文件权限错误

**解决方案：**
```bash
# macOS/Linux
chmod +x tools/generate.js

# Windows
# 以管理员身份运行命令提示符
```

### 问题：中文乱码

**解决方案：**
确保文件保存为UTF-8编码：
```bash
# 检查文件编码
file -I config.json

# 转换为UTF-8
iconv -f GBK -t UTF-8 config.json > config_utf8.json
```

## 最佳实践

1. **版本控制**：将生成的文件纳入版本控制
2. **备份配置**：定期备份重要的配置文件
3. **测试生成**：在部署前测试生成的网页
4. **文档更新**：更新配置文件时同步更新文档
5. **错误日志**：记录生成过程中的错误信息

## 未来改进

- [ ] 支持命令行参数
- [ ] 添加进度显示
- [ ] 支持批量生成
- [ ] 添加配置验证
- [ ] 支持自定义模板目录
- [ ] 添加生成日志
- [ ] 支持热重载
