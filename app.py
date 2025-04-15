from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from dotenv import load_dotenv
from services.youtube_service import YouTubeService
from services.ai_service import AIService

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGODB_URI")
app.secret_key = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
app.permanent_session_lifetime = timedelta(days=7)

# Initialize MongoDB
mongo = PyMongo(app)

# Initialize services
youtube_service = YouTubeService()
ai_service = AIService()

# Helper function to convert MongoDB objects to JSON serializable format
def parse_json(data):
    return json.loads(json.dumps(data, default=str))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = mongo.db.users.find_one({'email': email})
        
        if user and check_password_hash(user['password'], password):
            session.permanent = True
            session['user_id'] = str(user['_id'])
            session['email'] = user['email']
            session['name'] = user.get('name', '')
            return redirect(url_for('country_selector'))
        
        return render_template('login.html', error='Invalid email or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            return render_template('register.html', error='Email already exists')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        user_id = mongo.db.users.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password,
            'created_at': datetime.utcnow()
        }).inserted_id
        
        # Log the user in
        session.permanent = True
        session['user_id'] = str(user_id)
        session['email'] = email
        session['name'] = name
        
        return redirect(url_for('country_selector'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/country-selector')
def country_selector():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('country_selector.html')

@app.route('/trends')
def trends():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    region = request.args.get('region', 'US')
    
    # Get YouTube categories for the dropdown
    categories = youtube_service.get_categories()
    
    return render_template('trends.html', categories=categories, region=region)

@app.route('/generator')
def generator():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    topic = request.args.get('topic', '')
    region = request.args.get('region', 'US')
    category = request.args.get('category', '0')
    tags = request.args.get('tags', '[]')
    
    return render_template('generator.html', topic=topic, region=region, category=category, tags=tags)

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    scripts = list(mongo.db.scripts.find({'user_id': session['user_id']}).sort('created_at', -1))
    return render_template('history.html', scripts=scripts)

# API Routes
@app.route('/api/generate', methods=['POST'])
def generate_script():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    topic = data.get('topic')
    tone = data.get('tone', 'informative')
    length = data.get('length', 1000)
    region = data.get('region', 'US')
    category = data.get('category', '0')
    tags = data.get('tags', [])
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    # Get YouTube trend data to enhance the script
    trend_data = None
    if data.get('use_trends', True):
        trend_data = youtube_service.analyze_trends(region)
    
    # Generate script using Mistral 7B
    script = ai_service.generate_script(topic, tone, length, trend_data, tags, category)
    
    # Save to database
    script_id = mongo.db.scripts.insert_one({
        'user_id': session['user_id'],
        'title': topic,
        'content': script,
        'tone': tone,
        'length': len(script.split()),
        'region': region,
        'category': category,
        'tags': tags,
        'created_at': datetime.utcnow()
    }).inserted_id
    
    return jsonify({
        'script': script,
        'id': str(script_id)
    })

@app.route('/api/scripts', methods=['GET'])
def get_scripts():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    scripts = list(mongo.db.scripts.find({'user_id': session['user_id']}).sort('created_at', -1))
    
    # Convert ObjectId to string for JSON serialization
    for script in scripts:
        script['_id'] = str(script['_id'])
    
    return jsonify({'scripts': parse_json(scripts)})

@app.route('/api/scripts/<script_id>', methods=['GET'])
def get_script(script_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    script = mongo.db.scripts.find_one({'_id': ObjectId(script_id), 'user_id': session['user_id']})
    
    if not script:
        return jsonify({'error': 'Script not found'}), 404
    
    script['_id'] = str(script['_id'])
    return jsonify({'script': parse_json(script)})

@app.route('/api/trends', methods=['GET'])
def get_trends():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    region = request.args.get('region', 'US')
    category = request.args.get('category', '0')
    
    # Get trending videos from YouTube API
    if category == '0':
        # If "All" categories, get trend analysis
        trend_data = youtube_service.analyze_trends(region)
        return jsonify(trend_data)
    else:
        # If specific category, get trending videos
        videos = youtube_service.get_trending_videos(region, category, 10)
        return jsonify(videos)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = youtube_service.get_categories()
    return jsonify({'categories': categories})

if __name__ == '__main__':
    app.run(debug=True)
