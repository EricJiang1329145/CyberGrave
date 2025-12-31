from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.config['DATABASE'] = 'candles.db'

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据库"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS candles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/candles', methods=['GET'])
def get_candles():
    """获取所有蜡烛记录"""
    conn = get_db_connection()
    candles = conn.execute('SELECT * FROM candles ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return jsonify([{
        'id': candle['id'],
        'name': candle['name'],
        'message': candle['message'],
        'created_at': candle['created_at']
    } for candle in candles])

@app.route('/api/candles', methods=['POST'])
def add_candle():
    """添加蜡烛"""
    data = request.get_json()
    name = data.get('name', '匿名')
    message = data.get('message', '')
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO candles (name, message) VALUES (?, ?)',
        (name, message)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': '蜡烛已点亮'}), 201

@app.route('/api/candles/count', methods=['GET'])
def get_candle_count():
    """获取蜡烛总数"""
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) as count FROM candles').fetchone()['count']
    conn.close()
    
    return jsonify({'count': count})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
