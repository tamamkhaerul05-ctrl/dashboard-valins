from flask import Flask, jsonify
import urllib.request
import csv

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # Link export CSV publik dari Google Sheet Anda
        sheet_id = "1yofDpV-zKON5ne55PwRqlo4iNqQrrjmoeZrCm8IL-oc"
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        
        response = urllib.request.urlopen(csv_url)
        lines = [line.decode('utf-8') for line in response.readlines()]
        reader = csv.reader(lines)
        rows = list(reader)
        
        return jsonify({"status": "success", "data": rows})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)