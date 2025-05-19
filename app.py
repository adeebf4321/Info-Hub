from flask import Flask, render_template, request, jsonify
from utils.lookup import get_info_from_domain, get_info_from_ip, get_info_from_phone

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    data = request.json
    input_type = data.get('type')
    value = data.get('value')
    
    try:
        if input_type == 'domain':
            return jsonify(get_info_from_domain(value))
        elif input_type == 'ip':
            return jsonify(get_info_from_ip(value))
        elif input_type == 'phone':
            return jsonify(get_info_from_phone(value))
        else:
            return jsonify({'error': 'Invalid input type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
