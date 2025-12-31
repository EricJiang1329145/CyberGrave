const fs = require('fs');
const path = require('path');

const CONFIG_FILE = 'config.json';
const TEMPLATE_FILE = 'src/templates/template.html';
const THEME_FILE = 'src/themes/dark.css';
const SCRIPT_FILE = 'src/templates/script.js';
const OUTPUT_DIR = 'output';

function loadConfig() {
    try {
        const configData = fs.readFileSync(CONFIG_FILE, 'utf8');
        return JSON.parse(configData);
    } catch (error) {
        console.error('读取配置文件失败:', error.message);
        process.exit(1);
    }
}

function loadTemplate() {
    try {
        return fs.readFileSync(TEMPLATE_FILE, 'utf8');
    } catch (error) {
        console.error('读取模板文件失败:', error.message);
        process.exit(1);
    }
}

function loadTheme() {
    try {
        return fs.readFileSync(THEME_FILE, 'utf8');
    } catch (error) {
        console.error('读取主题文件失败:', error.message);
        process.exit(1);
    }
}

function loadScript() {
    try {
        return fs.readFileSync(SCRIPT_FILE, 'utf8');
    } catch (error) {
        console.error('读取脚本文件失败:', error.message);
        process.exit(1);
    }
}

function generatePhotosHTML(photos) {
    if (!photos || photos.length === 0) {
        return '<p class="no-photos">暂无照片</p>';
    }
    return photos.map(photo => `
        <div class="photo-item">
            <img src="${photo}" alt="照片" loading="lazy">
        </div>
    `).join('');
}

function generateTimelineHTML(timeline) {
    if (!timeline || timeline.length === 0) {
        return '<p class="no-timeline">暂无时间线</p>';
    }
    return timeline.map(item => `
        <div class="timeline-item">
            <div class="timeline-year">${item.year}</div>
            <div class="timeline-event">${item.event}</div>
        </div>
    `).join('');
}

function generateHTML(config) {
    let html = loadTemplate();

    const basic = config.basic || {};
    const theme = config.theme || {};
    const music = config.music || {};
    const candle = config.candle || {};
    const messages = config.messages || {};

    html = html.replace(/{{name}}/g, basic.name || '纪念对象');
    html = html.replace(/{{dates}}/g, basic.dates || '');
    html = html.replace(/{{subtitle}}/g, basic.subtitle || '');
    html = html.replace(/{{description}}/g, basic.description || '');

    html = html.replace(/{{photos}}/g, generatePhotosHTML(config.photos));
    html = html.replace(/{{timeline}}/g, generateTimelineHTML(config.timeline));

    html = html.replace(/{{candleTitle}}/g, candle.title || '点亮烛光');
    html = html.replace(/{{messagesTitle}}/g, messages.title || '访客留言');

    html = html.replace(/{{musicFile}}/g, music.file || '');

    if (!music.enabled) {
        html = html.replace(/<audio[^>]*>[\s\S]*?<\/audio>/, '');
    }

    if (!candle.enabled) {
        html = html.replace(/<section[^>]*id="candle-section"[^>]*>[\s\S]*?<\/section>/, '');
    }

    if (!messages.enabled) {
        html = html.replace(/<section[^>]*id="messages-section"[^>]*>[\s\S]*?<\/section>/, '');
    }

    return html;
}

function ensureOutputDir() {
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }
}

function copyAssets() {
    const assetsSource = 'src/assets';
    const assetsDest = path.join(OUTPUT_DIR, 'assets');

    if (fs.existsSync(assetsSource)) {
        if (!fs.existsSync(assetsDest)) {
            fs.mkdirSync(assetsDest, { recursive: true });
        }

        const files = fs.readdirSync(assetsSource);
        files.forEach(file => {
            const sourcePath = path.join(assetsSource, file);
            const destPath = path.join(assetsDest, file);

            if (fs.statSync(sourcePath).isFile()) {
                fs.copyFileSync(sourcePath, destPath);
                console.log(`复制资源文件: ${file}`);
            }
        });
    }
}

function generate() {
    console.log('🚀 开始生成赛博墓碑网页...\n');

    const config = loadConfig();
    console.log('✅ 配置文件加载成功');

    const html = generateHTML(config);
    console.log('✅ HTML 生成成功');

    const css = loadTheme();
    const js = loadScript();
    console.log('✅ 样式和脚本加载成功');

    ensureOutputDir();
    console.log('✅ 输出目录准备完成');

    fs.writeFileSync(path.join(OUTPUT_DIR, 'index.html'), html, 'utf8');
    fs.writeFileSync(path.join(OUTPUT_DIR, 'styles.css'), css, 'utf8');
    fs.writeFileSync(path.join(OUTPUT_DIR, 'script.js'), js, 'utf8');
    console.log('✅ 文件写入成功');

    copyAssets();
    console.log('✅ 资源文件复制完成');

    console.log('\n🎉 网页生成完成！');
    console.log(`📁 输出目录: ${path.resolve(OUTPUT_DIR)}`);
    console.log(`🌐 请在浏览器中打开: ${path.join(OUTPUT_DIR, 'index.html')}`);
}

if (require.main === module) {
    generate();
}

module.exports = { generate };
