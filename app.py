from flask import Flask, request, jsonify, send_file, render_template
import os
import uuid
from modules.parser import parse_file
from modules.ai_engine import generate_test_cases
from modules.excel_export import export_to_excel

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

GEMINI_API_KEY = "your_gemini_api_key_here"

os.makedirs('uploads', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        product  = request.form.get('product', 'PAM')
        feature  = request.form.get('feature', '')
        test_type = request.form.get('test_type', 'all')
        count    = int(request.form.get('count', 15))

        doc_text = ""
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                filename = str(uuid.uuid4()) + '_' + file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                doc_text = parse_file(filepath)
                os.remove(filepath)

        test_cases = generate_test_cases(
            product, feature, test_type, count, doc_text, GEMINI_API_KEY
        )

        output_filename = f"{product}_TestCases_{uuid.uuid4().hex[:6]}.xlsx"
        output_path = os.path.join('uploads', output_filename)
        export_to_excel(test_cases, product, output_path)

        return jsonify({
            'success': True,
            'count': len(test_cases),
            'download_url': f'/download/{output_filename}',
            'preview': test_cases[:3]
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join('uploads', filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)