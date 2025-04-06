from flask import Flask, request, send_file, jsonify
from test import upload_file, fetch_file
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask MongoDB GridFS app!"

# Route to upload a file
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_id = upload_file(file.filename, file)
    return jsonify({"message": "File uploaded", "file_id": str(file_id)}), 200

# Route to fetch a file
@app.route('/download/<file_name>', methods=['GET'])
def download(file_name):
    file_data = fetch_file(file_name)
    if file_data:
        return send_file(BytesIO(file_data), attachment_filename=file_name, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
