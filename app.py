from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, after_this_request
import os
import re
import json
import shutil
import zipfile
from datetime import datetime
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB 最大上传限制
app.config['UPLOAD_FOLDER'] = 'temp_uploads'
app.config['OUTPUT_FOLDER'] = 'temp_output'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ensure_dirs():
    """确保必要的目录存在"""
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def clean_temp_dirs():
    """清理临时目录"""
    for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)

def generate_config(data, photos, music_file):
    """生成配置文件"""
    config = {
        "basic": {
            "name": data.get('name', ''),
            "dates": data.get('dates', ''),
            "subtitle": data.get('subtitle', ''),
            "description": data.get('description', '')
        },
        "theme": {
            "name": "dark",
            "accentColor": data.get('accentColor', '#4a9eff')
        },
        "music": {
            "enabled": data.get('musicEnabled', False),
            "file": "assets/music.mp3" if music_file else "",
            "autoplay": data.get('musicAutoplay', False)
        },
        "photos": [f"assets/photo{i+1}.jpg" for i in range(len(photos))],
        "timeline": [],
        "messages": {
            "enabled": data.get('messagesEnabled', True),
            "title": "访客留言"
        },
        "candle": {
            "enabled": data.get('candleEnabled', True),
            "title": "点亮烛光"
        }
    }

    timeline_events = data.get('timelineEvents', [])
    for event in timeline_events:
        if event.get('year') and event.get('event'):
            config['timeline'].append({
                "year": event['year'],
                "event": event['event']
            })

    return config

def generate_html_from_template(config, template_path):
    """从模板生成 HTML"""
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()

    basic = config.get('basic', {})
    theme = config.get('theme', {})
    music = config.get('music', {})
    candle = config.get('candle', {})
    messages = config.get('messages', {})

    html = html.replace('{{name}}', basic.get('name', ''))
    html = html.replace('{{dates}}', basic.get('dates', ''))
    html = html.replace('{{subtitle}}', basic.get('subtitle', ''))
    html = html.replace('{{description}}', basic.get('description', ''))

    photos_html = ''
    for photo in config.get('photos', []):
        photos_html += f'''
        <div class="photo-item">
            <img src="{photo}" alt="照片" loading="lazy">
        </div>
    '''
    html = html.replace('{{photos}}', photos_html)

    timeline_html = ''
    for item in config.get('timeline', []):
        timeline_html += f'''
        <div class="timeline-item">
            <div class="timeline-year">{item['year']}</div>
            <div class="timeline-event">{item['event']}</div>
        </div>
    '''
    html = html.replace('{{timeline}}', timeline_html)

    html = html.replace('{{candleTitle}}', candle.get('title', '点亮烛光'))
    html = html.replace('{{messagesTitle}}', messages.get('title', '访客留言'))
    html = html.replace('{{musicFile}}', music.get('file', ''))

    if not music.get('enabled'):
        html = re.sub(r'<audio[^>]*>[\s\S]*?</audio>', '', html, flags=re.DOTALL)

    if not candle.get('enabled'):
        html = re.sub(r'<section[^>]*id="candle-section"[^>]*>[\s\S]*?</section>', '', html, flags=re.DOTALL)

    if not messages.get('enabled'):
        html = re.sub(r'<section[^>]*id="messages-section"[^>]*>[\s\S]*?</section>', '', html, flags=re.DOTALL)

    return html

@app.route('/')
def index():
    """主页"""
    return render_template('generator.html')

@app.route('/generate', methods=['POST'])
def generate():
    """生成纪念页面"""
    try:
        clean_temp_dirs()
        ensure_dirs()

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        session_id = f"session_{timestamp}"
        session_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(session_dir, exist_ok=True)

        data = request.form.to_dict()

        photos = []
        photo_files = request.files.getlist('photos')
        for i, photo in enumerate(photo_files):
            if photo and photo.filename:
                filename = f"photo{i+1}.jpg"
                photo_path = os.path.join(session_dir, 'assets', filename)
                os.makedirs(os.path.dirname(photo_path), exist_ok=True)
                photo.save(photo_path)
                photos.append(photo_path)

        music_file = None
        music = request.files.get('music')
        if music and music.filename:
            music_path = os.path.join(session_dir, 'assets', 'music.mp3')
            os.makedirs(os.path.dirname(music_path), exist_ok=True)
            music.save(music_path)
            music_file = music_path

        config = generate_config(data, photos, music_file)

        template_path = os.path.join(BASE_DIR, 'src', 'templates', 'template.html')
        html_content = generate_html_from_template(config, template_path)

        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
        os.makedirs(output_dir, exist_ok=True)

        with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)

        theme_path = os.path.join(BASE_DIR, 'src', 'themes', 'dark.css')
        shutil.copy(theme_path, os.path.join(output_dir, 'styles.css'))

        script_path = os.path.join(BASE_DIR, 'src', 'templates', 'script.js')
        shutil.copy(script_path, os.path.join(output_dir, 'script.js'))

        if os.path.exists(os.path.join(session_dir, 'assets')):
            shutil.copytree(os.path.join(session_dir, 'assets'),
                          os.path.join(output_dir, 'assets'),
                          dirs_exist_ok=True)

        zip_path = os.path.join(app.config['OUTPUT_FOLDER'], f'cyber_grave_{timestamp}.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, arcname)

        @after_this_request
        def remove_file(response):
            try:
                if os.path.exists(zip_path):
                    os.remove(zip_path)
            except Exception as e:
                print(f"清理文件失败: {e}")
            return response

        return send_file(zip_path, as_attachment=True,
                        download_name=f'cyber_grave_{timestamp}.zip',
                        mimetype='application/zip')

    except Exception as e:
        print(f"生成失败: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/preview', methods=['POST'])
def preview():
    """预览页面"""
    try:
        clean_temp_dirs()
        ensure_dirs()

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        session_id = f"preview_{timestamp}"
        session_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(session_dir, exist_ok=True)

        data = request.form.to_dict()

        photos = []
        photo_files = request.files.getlist('photos')
        for i, photo in enumerate(photo_files):
            if photo and photo.filename:
                filename = f"photo{i+1}.jpg"
                photo_path = os.path.join(session_dir, 'assets', filename)
                os.makedirs(os.path.dirname(photo_path), exist_ok=True)
                photo.save(photo_path)
                photos.append(photo_path)

        music_file = None
        music = request.files.get('music')
        if music and music.filename:
            music_path = os.path.join(session_dir, 'assets', 'music.mp3')
            os.makedirs(os.path.dirname(music_path), exist_ok=True)
            music.save(music_path)
            music_file = music_path

        config = generate_config(data, photos, music_file)

        template_path = os.path.join(BASE_DIR, 'src', 'templates', 'template.html')
        html_content = generate_html_from_template(config, template_path)

        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
        os.makedirs(output_dir, exist_ok=True)

        with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)

        theme_path = os.path.join(BASE_DIR, 'src', 'themes', 'dark.css')
        shutil.copy(theme_path, os.path.join(output_dir, 'styles.css'))

        script_path = os.path.join(BASE_DIR, 'src', 'templates', 'script.js')
        shutil.copy(script_path, os.path.join(output_dir, 'script.js'))

        if os.path.exists(os.path.join(session_dir, 'assets')):
            shutil.copytree(os.path.join(session_dir, 'assets'),
                          os.path.join(output_dir, 'assets'),
                          dirs_exist_ok=True)

        return render_template('preview.html', session_id=session_id)

    except Exception as e:
        print(f"预览失败: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/preview/<session_id>')
def view_preview(session_id):
    """查看预览"""
    return send_from_directory(os.path.join(app.config['OUTPUT_FOLDER'], session_id), 'index.html')

@app.route('/preview_assets/<session_id>/<path:filename>')
def preview_assets(session_id, filename):
    """预览资源文件"""
    return send_from_directory(os.path.join(app.config['OUTPUT_FOLDER'], session_id, 'assets'), filename)

if __name__ == '__main__':
    ensure_dirs()
    app.run(debug=True, port=5000)
