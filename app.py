from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import gspread
import time
import os

app = Flask(__name__)
CORS(app)

cached_data = None
last_fetch_time = 0
CACHE_DURATION = 60  # Cache selama 1 menit

# Route untuk menyajikan halaman utama (index.html)
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    global cached_data, last_fetch_time
    current_time = time.time()
    
    if cached_data and (current_time - last_fetch_time < CACHE_DURATION):
        return jsonify({"status": "success", "data": cached_data, "source": "cache"}), 200

    try:
        gc = gspread.service_account(filename='credentials.json')
        spreadsheet_id = '1yofDpV-zKON5ne55PwRqlo4iNqQrrjmoeZrCm8IL-oc'
        spreadsheet = gc.open_by_key(spreadsheet_id)
        
        worksheet = spreadsheet.worksheet('Master DASHBOARD')
        rows = worksheet.get_all_values()
        
        cached_data = rows
        last_fetch_time = current_time
        
        return jsonify({"status": "success", "data": rows, "source": "sheets"}), 200
    except Exception as e:
        if cached_data:
            return jsonify({"status": "success", "data": cached_data, "source": "fallback-cache"}), 200
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)