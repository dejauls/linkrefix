from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

client = MongoClient('mongodb://belajar:belajar@ac-pewhlve-shard-00-00.m1k88nt.mongodb.net:27017,ac-pewhlve-shard-00-01.m1k88nt.mongodb.net:27017,ac-pewhlve-shard-00-02.m1k88nt.mongodb.net:27017/?ssl=true&replicaSet=atlas-i3tctf-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')
db = client.linkc

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/link", methods=["POST"])
def link_post():
    try:
        platform = request.form['platform']
        print(f"Received platform: {platform}") 
        
        current_time = datetime.now().strftime('%Y-%m-%d')  
        doc = {
            'platform': platform,
            'timestamp': current_time  
        }

        result = db.link.insert_one(doc)
        print(f"Document inserted with id: {result.inserted_id}")  # Debug: Print insertion result

        return jsonify({'msg': 'POST request received!'})
    except Exception as e:
        print(f"Error: {e}")  # Debug: Print any error that occurs
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/view_data', methods=['GET'])
def view_data():
    try:
        date = request.args.get('date')
        query = {}
        if date:
            query['timestamp'] = date
        
        data = list(db.link.find(query, {'_id': 0, 'platform': 1, 'timestamp': 1}))
        return render_template('index.html', data=data)
    except Exception as e:
        print(f"Error: {e}")  # Debug: Print any error that occurs
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500
    
@app.route('/data_today', methods=['GET'])
def data_today():
    try:
        today = datetime.today().strftime('%Y-%m-%d')
        data = list(db.link.find({'timestamp': today}, {'_id': 0, 'platform': 1, 'timestamp': 1}))
        return jsonify(data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500    
    
@app.route('/data_month', methods=['GET'])
def data_month():
    try:
        today = datetime.today()
        first_day_of_month = today.replace(day=1)
        data = list(db.link.find({'timestamp': {'$gte': first_day_of_month.strftime('%Y-%m-%d')}}, {'_id': 0, 'platform': 1, 'timestamp': 1}))
        return jsonify(data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/data_week', methods=['GET'])
def data_week():
    try:
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        data = list(db.link.find({'timestamp': {'$gte': start_of_week.strftime('%Y-%m-%d')}}, {'_id': 0, 'platform': 1, 'timestamp': 1}))
        return jsonify(data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500    

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
