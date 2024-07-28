from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import pytz

load_dotenv()  # Load environment variables from .env

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/visitor')
def home():
    return render_template('index.html')

@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/')
def halaman():
    return render_template('jembatan.html')

@app.route("/link", methods=["POST"])
def link_post():
    try:
        platform = request.form.get('platform')  # Use get() to avoid KeyError
        print(f"Received platform: {platform}")
        timezone = pytz.timezone("Asia/Jakarta")
        current_time = datetime.now(timezone)
        link = Link(platform=platform, timestamp=current_time)
        db.session.add(link)
        db.session.commit()
        print(f"Document inserted with id: {link.id}")
        return jsonify({'msg': 'POST request received!'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500


@app.route('/data_date_range', methods=['GET'])
def data_date_range():
    try:
        start_date = request.args.get('start')
        end_date = request.args.get('end')
        if not start_date or not end_date:
            return jsonify({"error": "Start and end date parameters are required"}), 400

        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        data = Link.query.filter(Link.timestamp.between(start_date_obj, end_date_obj)).all()
        result = [{'platform': entry.platform, 'timestamp': entry.timestamp.strftime('%Y-%m-%d')} for entry in data]
        return jsonify(result)
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/view_data', methods=['GET'])
def view_data():
    try:
        date = request.args.get('date')
        query = Link.query
        if date:
            query = query.filter_by(timestamp=datetime.strptime(date, '%Y-%m-%d'))

        data = query.all()
        result = [{'platform': entry.platform, 'timestamp': entry.timestamp.strftime('%Y-%m-%d')} for entry in data]
        return render_template('index.html', data=result)
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/data_today', methods=['GET'])
def data_today():
    try:
        timezone = pytz.timezone("Asia/Jakarta")
        today = datetime.now(timezone).strftime('%Y-%m-%d')
        data = Link.query.filter(db.func.date(Link.timestamp) == today).all()
        result = [{'platform': entry.platform, 'timestamp': entry.timestamp.strftime('%Y-%m-%d')} for entry in data]
        return jsonify(result)
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/data_month', methods=['GET'])
def data_month():
    try:
        timezone = pytz.timezone("Asia/Jakarta")
        today = datetime.now(timezone)
        first_day_of_month = today.replace(day=1)
        data = Link.query.filter(Link.timestamp >= first_day_of_month).all()
        result = [{'platform': entry.platform, 'timestamp': entry.timestamp.strftime('%Y-%m-%d')} for entry in data]
        return jsonify(result)
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/data_week', methods=['GET'])
def data_week():
    try:
        timezone = pytz.timezone("Asia/Jakarta")
        today = datetime.now(timezone)
        start_of_week = today - timedelta(days=today.weekday())
        data = Link.query.filter(Link.timestamp >= start_of_week).all()
        result = [{'platform': entry.platform, 'timestamp': entry.timestamp.strftime('%Y-%m-%d')} for entry in data]
        return jsonify(result)
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/instagram_count', methods=['GET'])
def instagram_count():
    try:
        count = Link.query.filter_by(platform='instagram').count()
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/whatsapp_count', methods=['GET'])
def whatsapp_count():
    try:
        count = Link.query.filter_by(platform='whatsapp').count()
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/tiktok_count', methods=['GET'])
def tiktok_count():
    try:
        count = Link.query.filter_by(platform='tiktok').count()
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/youtube_count', methods=['GET'])
def youtube_count():
    try:
        count = Link.query.filter_by(platform='youtube').count()
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/website_count', methods=['GET'])
def website_count():
    try:
        count = Link.query.filter_by(platform='website').count()
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/berita_count', methods=['GET'])
def berita_count():
    try:
        count = Link.query.filter_by(platform='berita').count()
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/artikel_count', methods=['GET'])
def artikel_count():
    try:
        count = Link.query.filter_by(platform='artikel').count()
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/data_range', methods=['GET'])
def data_range():
    try:
        start_date = request.args.get('start')
        end_date = request.args.get('end')
        
        if not start_date or not end_date:
            return jsonify({'msg': 'Start date and end date are required'}), 400
        
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        
        platforms = ['instagram', 'whatsapp', 'tiktok', 'youtube', 'website', 'berita', 'artikel']
        counts = {}

        for platform in platforms:
            count = Link.query.filter_by(platform=platform).filter(Link.timestamp.between(start_date_obj, end_date_obj)).count()
            counts[platform] = count
        
        return jsonify(counts)
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

def get_month_data(year, month):
    from calendar import monthrange
    num_days = monthrange(year, month)[1]
    start_date = datetime(year, month, 1).strftime('%Y-%m-%d')
    end_date = datetime(year, month, num_days).strftime('%Y-%m-%d')

    data = Link.query.filter(Link.timestamp.between(start_date, end_date)).all()

    # Prepare chart data structure
    chart_data = {}

    # Initialize data structure with all days of the month
    for platform in ['artikel', 'berita', 'instagram', 'tiktok', 'website', 'whatsapp', 'youtube']:
        chart_data[platform] = {
            'labels': [datetime(year, month, day).strftime('%Y-%m-%d') for day in range(1, num_days + 1)],
            'data': [0] * num_days
        }

    # Fill data from MySQL results
    for entry in data:
        platform = entry.platform
        date = entry.timestamp.strftime('%Y-%m-%d')
        count = 1

        if date in chart_data[platform]['labels']:
            index = chart_data[platform]['labels'].index(date)
            chart_data[platform]['data'][index] += count

    return chart_data

@app.route('/data_total', methods=['GET'])
def data_total():
    try:
        platforms = ['instagram', 'whatsapp', 'youtube', 'website', 'artikel', 'berita', 'tiktok']
        counts = {}

        for platform in platforms:
            count = Link.query.filter_by(platform=platform).count()
            counts[platform] = count
        
        return jsonify(counts)
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

@app.route('/total_semuadata', methods=['GET'])
def semuadata():
    try:
        timezone = pytz.timezone("Asia/Jakarta")
        today = datetime.now(timezone)
        last_week = today - timedelta(days=7)
        
        total_count = Link.query.count()
        previous_week_count = Link.query.filter(Link.timestamp < last_week).count()
        
        return jsonify({'total_count': total_count, 'previous_week_count': previous_week_count})
    except Exception as e:
        return jsonify({'msg': 'An error occurred', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
