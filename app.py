from flask import Flask, request, jsonify, render_template
import os
import random
import time
from datetime import datetime, timedelta

app = Flask(__name__)

# 简单配置
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    """简化版文件上传"""
    print("收到上传请求")
    
    try:
        # 检查是否有文件
        if 'video' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['video']
        
        # 检查文件名
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 生成安全文件名
        filename = f"video_{int(time.time())}_{random.randint(1000,9999)}.mp4"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        print(f"保存文件到: {filepath}")
        
        # 保存文件
        file.save(filepath)
        
        # 返回成功响应
        return jsonify({
            'success': True,
            'filename': filename,
            'message': '上传成功'
        })
        
    except Exception as e:
        print(f"上传错误: {str(e)}")
        return jsonify({'error': f'上传失败: {str(e)}'}), 500

@app.route('/analyze', methods=['POST'])
def analyze_video():
    """简化版视频分析"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'error': '缺少文件名'}), 400
        
        print(f"分析视频: {filename}")
        
        # 模拟分析过程
        time.sleep(3)
        
        # 生成模拟数据
        violations = generate_mock_violations()
        traffic_flow = generate_mock_traffic_flow()
        accident_probability = calculate_accident_probability(violations)
        
        return jsonify({
            'success': True,
            'results': {
                'violations': violations,
                'traffic_flow': traffic_flow,
                'accident_probability': accident_probability,
                'real_time_stats': {
                    'vehicle_count': sum(flow['vehicle_count'] for flow in traffic_flow.values()),
                    'average_speed': 45,
                    'violation_count': len(violations),
                    'red_light_violations': len([v for v in violations if 'red_light' in v['type']]),
                    'reverse_violations': len([v for v in violations if 'reverse' in v['type']]),
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                }
            }
        })
        
    except Exception as e:
        print(f"分析错误: {str(e)}")
        return jsonify({'error': f'分析失败: {str(e)}'}), 500

def generate_mock_violations():
    """生成模拟违规数据"""
    violations = []
    
    # 随机生成一些违规
    violation_types = [
        {'type': 'speeding', 'desc': '超速行驶', 'severity': 'high'},
        {'type': 'run_red_light', 'desc': '闯红灯', 'severity': 'high'},
        {'type': 'reverse_driving', 'desc': '逆向行驶', 'severity': 'high'},
        {'type': 'no_pedestrian_yield', 'desc': '未礼让行人', 'severity': 'medium'},
        {'type': 'run_yellow_light', 'desc': '黄灯加速', 'severity': 'medium'}
    ]
    
    num_violations = random.randint(2, 6)
    
    for i in range(num_violations):
        violation = random.choice(violation_types)
        violations.append({
            'type': violation['type'],
            'license_plate': generate_license_plate(),
            'description': violation['desc'],
            'severity': violation['severity'],
            'timestamp': (datetime.now() - timedelta(minutes=random.randint(1,30))).strftime('%H:%M:%S'),
            'location': random.choice(['南北路口', '东西路口', '人行横道', '十字路口中心'])
        })
    
    return violations

def generate_mock_traffic_flow():
    """生成模拟车流量数据"""
    directions = ['north', 'south', 'east', 'west']
    flow_data = {}
    
    for direction in directions:
        flow_data[direction] = {
            'vehicle_count': random.randint(50, 200),
            'average_speed': random.randint(30, 70)
        }
    
    return flow_data

def calculate_accident_probability(violations):
    """计算事故概率"""
    base_probability = 5
    violation_penalty = len(violations) * 3
    high_severity_penalty = len([v for v in violations if v['severity'] == 'high']) * 10
    
    total = base_probability + violation_penalty + high_severity_penalty
    return min(total, 100)

def generate_license_plate():
    """生成车牌号"""
    provinces = ['京', '沪', '粤', '川', '浙']
    letters = 'ABCDEFGHJK'
    numbers = ''.join([str(random.randint(0,9)) for _ in range(5)])
    
    return f"{random.choice(provinces)}{random.choice(letters)}{numbers}"

if __name__ == '__main__':
    print("=== 交通风险预警系统启动 ===")
    print("访问: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)