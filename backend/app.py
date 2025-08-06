import os
import uuid
import jwt
import sqlite3
import datetime
import time
from functools import wraps
from flask import Flask, request, jsonify, g, render_template_string
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from github_integration import GitHubIntegration, IssueProposal

# Load environment variables
load_dotenv()

# Debug: Check if environment variables are loaded
print("Environment variables check:")
print(f"GITHUB_TOKEN: {'Set' if os.environ.get('GITHUB_TOKEN') else 'Not set'}")
print(f"SECRET_KEY: {'Set' if os.environ.get('SECRET_KEY') else 'Not set'}")

# Initialize app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'db.sqlite')

# Mail configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.example.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'username')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@example.com')

mail = Mail(app)

# Console log capture system
console_logs = []
MAX_LOGS = 100

def add_log(level, message, endpoint=None, user=None):
    """Add a log entry to the console logs"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        'timestamp': timestamp,
        'level': level,
        'message': message,
        'endpoint': endpoint,
        'user': user
    }
    console_logs.append(log_entry)
    
    # Keep only the last MAX_LOGS entries
    if len(console_logs) > MAX_LOGS:
        console_logs.pop(0)
    
    # Also print to console
    print(f"[{timestamp}] {level.upper()}: {message}")

# Add initial startup log
add_log('info', 'Atim Backend Server Starting...')

# Database setup
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as f:
            db.executescript(f.read())

# Create database tables if they don't exist
def create_tables():
    db = get_db()
    cursor = db.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        verified INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create email_tokens table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS email_tokens (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        token TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # Create issues table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS issues (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT NOT NULL,
        file_path TEXT NOT NULL,
        line_number INTEGER NOT NULL,
        suggested_fix TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create pull_requests table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pull_requests (
        id TEXT PRIMARY KEY,
        github_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL,
        diff TEXT,
        html_url TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create feedback table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id TEXT PRIMARY KEY,
        pr_id TEXT NOT NULL,
        comment TEXT NOT NULL,
        approved INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pr_id) REFERENCES pull_requests (id)
    )
    ''')

    # Create chat_messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_messages (
        id TEXT PRIMARY KEY,
        sender TEXT NOT NULL,
        content TEXT NOT NULL,
        reference_id TEXT,
        reference_type TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    db.commit()

# Create tables on startup
with app.app_context():
    create_tables()

# Main dashboard route
@app.route('/')
def dashboard():
    """Main dashboard showing backend status, logs, and API documentation"""
    add_log('info', 'Dashboard accessed', endpoint='/')
    
    # API Documentation
    api_docs = {
        'Authentication': {
            'POST /api/register': 'Register a new user',
            'POST /api/login': 'Login user',
            'GET /api/user': 'Get current user (requires auth)',
            'GET /api/verify': 'Verify email with token'
        },
        'Issues & PRs': {
            'GET /api/issues': 'Get all issues (requires auth)',
            'GET /api/issues/<id>': 'Get specific issue (requires auth)',
            'GET /api/prs': 'Get all pull requests (requires auth)',
            'GET /api/prs/<id>': 'Get specific PR (requires auth)',
            'POST /api/prs/<id>/feedback': 'Submit PR feedback (requires auth)'
        },
        'Chat': {
            'GET /api/chat': 'Get chat messages (requires auth)',
            'POST /api/chat': 'Send chat message (requires auth)'
        },
        'Demo Endpoints': {
            'GET /api/demo/issues': 'Get demo issues (no auth required)',
            'GET /api/demo/chat': 'Get demo chat messages (no auth required)',
            'POST /api/demo/chat': 'Send demo chat message (no auth required)'
        },
        'GitHub Integration': {
            'GET /api/github/proposals': 'Get issue proposals',
            'POST /api/github/proposals/<id>/approve': 'Approve and create GitHub issue',
            'POST /api/github/proposals/<id>/reject': 'Reject issue proposal',
            'GET /api/github/stats': 'Get repository statistics'
        },
        'Public': {
            'GET /api/kanban': 'Get kanban board items'
        }
    }
    
    # Server stats
    server_stats = {
        'uptime': 'Running',
        'version': '1.0.0',
        'port': 5070,
        'environment': 'Development',
        'database': 'SQLite',
        'cors_enabled': True,
        'mail_enabled': bool(app.config['MAIL_USERNAME']),
        'github_integration': True
    }
    
    # HTML template for the dashboard
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Atim Backend Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            .log-entry { font-family: 'Courier New', monospace; }
            .log-info { color: #3b82f6; }
            .log-warning { color: #f59e0b; }
            .log-error { color: #ef4444; }
            .log-success { color: #10b981; }
        </style>
    </head>
    <body class="bg-slate-900 text-white min-h-screen">
        <!-- Header -->
        <div class="bg-slate-800 border-b border-slate-700">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div class="flex items-center justify-between">
                    <div>
                        <h1 class="text-3xl font-bold text-white">Atim Backend Dashboard</h1>
                        <p class="text-slate-400 mt-2">Real-time monitoring and API documentation</p>
                    </div>
                    <div class="flex items-center space-x-4">
                        <div class="flex items-center space-x-2">
                            <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                            <span class="text-green-400 font-medium">Backend is Running</span>
                        </div>
                        <div class="text-sm text-slate-400">
                            Port: {{ server_stats.port }}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Server Stats -->
                <div class="lg:col-span-1">
                    <div class="bg-slate-800 rounded-lg p-6 border border-slate-700">
                        <h2 class="text-xl font-semibold text-white mb-4">Server Status</h2>
                        <div class="space-y-3">
                            {% for key, value in server_stats.items() %}
                            <div class="flex justify-between">
                                <span class="text-slate-400 capitalize">{{ key.replace('_', ' ') }}:</span>
                                <span class="text-white font-medium">{{ value }}</span>
                            </div>
                            {% endfor %}
                        </div>
                    </div>

                    <!-- API Documentation -->
                    <div class="bg-slate-800 rounded-lg p-6 border border-slate-700 mt-6">
                        <h2 class="text-xl font-semibold text-white mb-4">API Documentation</h2>
                        <div class="space-y-4">
                            {% for category, endpoints in api_docs.items() %}
                            <div>
                                <h3 class="text-lg font-medium text-blue-400 mb-2">{{ category }}</h3>
                                <div class="space-y-2">
                                    {% for endpoint, description in endpoints.items() %}
                                    <div class="bg-slate-700 rounded p-2">
                                        <div class="text-sm font-mono text-green-400">{{ endpoint }}</div>
                                        <div class="text-xs text-slate-300 mt-1">{{ description }}</div>
                                    </div>
                                    {% endfor %}
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>

                <!-- Console Logs -->
                <div class="lg:col-span-2">
                    <div class="bg-slate-800 rounded-lg border border-slate-700">
                        <div class="flex items-center justify-between p-6 border-b border-slate-700">
                            <h2 class="text-xl font-semibold text-white">Console Logs</h2>
                            <div class="flex items-center space-x-2">
                                <span class="text-sm text-slate-400">{{ console_logs|length }} entries</span>
                                <button onclick="location.reload()" class="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">
                                    Refresh
                                </button>
                            </div>
                        </div>
                        <div class="h-96 overflow-y-auto p-4 bg-slate-900">
                            {% for log in console_logs|reverse %}
                            <div class="log-entry text-sm mb-2 p-2 bg-slate-800 rounded border-l-4 border-slate-600">
                                <div class="flex items-center justify-between">
                                    <span class="text-slate-400">{{ log.timestamp }}</span>
                                    <span class="px-2 py-1 rounded text-xs font-medium
                                        {% if log.level == 'info' %}bg-blue-900 text-blue-300
                                        {% elif log.level == 'warning' %}bg-yellow-900 text-yellow-300
                                        {% elif log.level == 'error' %}bg-red-900 text-red-300
                                        {% elif log.level == 'success' %}bg-green-900 text-green-300
                                        {% else %}bg-gray-900 text-gray-300{% endif %}">
                                        {{ log.level.upper() }}
                                    </span>
                                </div>
                                <div class="text-white mt-1">{{ log.message }}</div>
                                {% if log.endpoint %}
                                <div class="text-slate-400 text-xs mt-1">Endpoint: {{ log.endpoint }}</div>
                                {% endif %}
                                {% if log.user %}
                                <div class="text-slate-400 text-xs">User: {{ log.user }}</div>
                                {% endif %}
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // Auto-refresh logs every 5 seconds
            setInterval(() => {
                location.reload();
            }, 5000);
        </script>
    </body>
    </html>
    '''
    
    return render_template_string(html_template, 
                                console_logs=console_logs,
                                server_stats=server_stats,
                                api_docs=api_docs)

# JWT token verification
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({
                'success': False,
                'error': 'Authentication token is missing!'
            }), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            db = get_db()
            user = db.execute('SELECT * FROM users WHERE id = ?', (data['user_id'],)).fetchone()

            if not user:
                return jsonify({
                    'success': False,
                    'error': 'Invalid authentication token!'
                }), 401

            # Check if user is verified
            if not user['verified']:
                return jsonify({
                    'success': False,
                    'error': 'Email not verified!'
                }), 403

        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Invalid authentication token!'
            }), 401

        return f(user, *args, **kwargs)

    return decorated

# Generate a verification token
def generate_verification_token(user_id):
    token = str(uuid.uuid4())
    db = get_db()
    db.execute(
        'INSERT INTO email_tokens (id, user_id, token) VALUES (?, ?, ?)',
        (str(uuid.uuid4()), user_id, token)
    )
    db.commit()
    return token

# Send verification email
def send_verification_email(email, token):
    verification_url = f"http://localhost:5173/verify?token={token}"
    subject = "Verify your email for Atim Assistant"

    html_content = f"""
    <html>
        <body>
            <h2>Welcome to Atim Assistant!</h2>
            <p>Thank you for signing up. Please verify your email address by clicking the link below:</p>
            <p><a href="{verification_url}">Verify Email</a></p>
            <p>If you didn't sign up for an account, please ignore this email.</p>
        </body>
    </html>
    """

    try:
        msg = Message(
            subject=subject,
            recipients=[email],
            html=html_content
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

# Routes
@app.route('/api/register', methods=['POST'])
def register():
    add_log('info', f'Registration attempt for email: {request.get_json().get("email", "unknown")}', endpoint='/api/register')
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        add_log('warning', 'Registration failed: Missing email or password', endpoint='/api/register')
        return jsonify({
            'success': False,
            'error': 'Email and password are required!'
        }), 400

    email = data['email']
    password = data['password']

    # Check if email already exists
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

    if user:
        add_log('warning', f'Registration failed: Email already exists - {email}', endpoint='/api/register')
        return jsonify({
            'success': False,
            'error': 'Email already registered!'
        }), 400

    # Create new user
    user_id = str(uuid.uuid4())
    password_hash = generate_password_hash(password)

    db.execute(
        'INSERT INTO users (id, email, password_hash) VALUES (?, ?, ?)',
        (user_id, email, password_hash)
    )
    db.commit()

    # Generate and send verification token
    token = generate_verification_token(user_id)
    if not send_verification_email(email, token):
        return jsonify({
            'success': False,
            'error': 'Failed to send verification email, but account was created!'
        }), 500

    add_log('success', f'User registered successfully: {email}', endpoint='/api/register')
    return jsonify({
        'success': True,
        'data': {
            'message': 'User registered successfully. Please check your email to verify your account.'
        }
    }), 201

@app.route('/api/verify', methods=['GET'])
def verify_email():
    token = request.args.get('token')

    if not token:
        return jsonify({
            'success': False,
            'error': 'Verification token is required!'
        }), 400

    db = get_db()
    token_record = db.execute('SELECT * FROM email_tokens WHERE token = ?', (token,)).fetchone()

    if not token_record:
        return jsonify({
            'success': False,
            'error': 'Invalid verification token!'
        }), 400

    # Check if token is older than 24 hours
    token_created_at = datetime.datetime.fromisoformat(token_record['created_at'].replace('Z', '+00:00'))
    if (datetime.datetime.now() - token_created_at).days > 1:
        return jsonify({
            'success': False,
            'error': 'Verification token has expired!'
        }), 400

    # Update user as verified
    db.execute('UPDATE users SET verified = 1 WHERE id = ?', (token_record['user_id'],))

    # Remove the token
    db.execute('DELETE FROM email_tokens WHERE token = ?', (token,))
    db.commit()

    return jsonify({
        'success': True,
        'data': {
            'message': 'Email verified successfully!'
        }
    }), 200

@app.route('/api/login', methods=['POST'])
def login():
    add_log('info', f'Login attempt for email: {request.get_json().get("email", "unknown")}', endpoint='/api/login')
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        add_log('warning', 'Login failed: Missing email or password', endpoint='/api/login')
        return jsonify({
            'success': False,
            'error': 'Email and password are required!'
        }), 400

    email = data['email']
    password = data['password']

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({
            'success': False,
            'error': 'Invalid email or password!'
        }), 401

    # Generate JWT token
    token = jwt.encode(
        {
            'user_id': user['id'],
            'email': user['email'],
            'exp': datetime.datetime.now() + datetime.timedelta(days=1)
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify({
        'success': True,
        'data': {
            'token': token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'verified': user['verified'] == 1
            }
        }
    }), 200

@app.route('/api/user', methods=['GET'])
@token_required
def get_user(user):
    return jsonify({
        'success': True,
        'data': {
            'id': user['id'],
            'email': user['email'],
            'verified': user['verified'] == 1
        }
    }), 200

# Issues endpoints
@app.route('/api/issues', methods=['GET'])
@token_required
def get_issues(user):
    db = get_db()
    issues = db.execute('SELECT * FROM issues ORDER BY created_at DESC').fetchall()

    issues_list = []
    for issue in issues:
        issues_list.append({
            'id': issue['id'],
            'title': issue['title'],
            'description': issue['description'],
            'severity': issue['severity'],
            'status': issue['status'],
            'file_path': issue['file_path'],
            'line_number': issue['line_number'],
            'suggested_fix': issue['suggested_fix'],
            'created_at': issue['created_at'],
            'updated_at': issue['updated_at']
        })

    return jsonify({
        'success': True,
        'data': issues_list
    }), 200

@app.route('/api/issues/<issue_id>', methods=['GET'])
@token_required
def get_issue(user, issue_id):
    db = get_db()
    issue = db.execute('SELECT * FROM issues WHERE id = ?', (issue_id,)).fetchone()

    if not issue:
        return jsonify({
            'success': False,
            'error': 'Issue not found!'
        }), 404

    return jsonify({
        'success': True,
        'data': {
            'id': issue['id'],
            'title': issue['title'],
            'description': issue['description'],
            'severity': issue['severity'],
            'status': issue['status'],
            'file_path': issue['file_path'],
            'line_number': issue['line_number'],
            'suggested_fix': issue['suggested_fix'],
            'created_at': issue['created_at'],
            'updated_at': issue['updated_at']
        }
    }), 200

# Pull Requests endpoints
@app.route('/api/prs', methods=['GET'])
@token_required
def get_pull_requests(user):
    db = get_db()
    prs = db.execute('SELECT * FROM pull_requests ORDER BY created_at DESC').fetchall()

    prs_list = []
    for pr in prs:
        # Get feedback for this PR
        feedback = db.execute('SELECT * FROM feedback WHERE pr_id = ?', (pr['id'],)).fetchall()
        feedback_list = []

        for fb in feedback:
            feedback_list.append({
                'id': fb['id'],
                'pr_id': fb['pr_id'],
                'comment': fb['comment'],
                'approved': fb['approved'] == 1,
                'created_at': fb['created_at']
            })

        prs_list.append({
            'id': pr['id'],
            'github_id': pr['github_id'],
            'title': pr['title'],
            'description': pr['description'],
            'status': pr['status'],
            'diff': pr['diff'],
            'html_url': pr['html_url'],
            'created_at': pr['created_at'],
            'updated_at': pr['updated_at'],
            'feedback': feedback_list
        })

    return jsonify({
        'success': True,
        'data': prs_list
    }), 200

@app.route('/api/prs/<pr_id>', methods=['GET'])
@token_required
def get_pull_request(user, pr_id):
    db = get_db()
    pr = db.execute('SELECT * FROM pull_requests WHERE id = ?', (pr_id,)).fetchone()

    if not pr:
        return jsonify({
            'success': False,
            'error': 'Pull request not found!'
        }), 404

    # Get feedback for this PR
    feedback = db.execute('SELECT * FROM feedback WHERE pr_id = ?', (pr_id,)).fetchall()
    feedback_list = []

    for fb in feedback:
        feedback_list.append({
            'id': fb['id'],
            'pr_id': fb['pr_id'],
            'comment': fb['comment'],
            'approved': fb['approved'] == 1,
            'created_at': fb['created_at']
        })

    return jsonify({
        'success': True,
        'data': {
            'id': pr['id'],
            'github_id': pr['github_id'],
            'title': pr['title'],
            'description': pr['description'],
            'status': pr['status'],
            'diff': pr['diff'],
            'html_url': pr['html_url'],
            'created_at': pr['created_at'],
            'updated_at': pr['updated_at'],
            'feedback': feedback_list
        }
    }), 200

@app.route('/api/prs/<pr_id>/feedback', methods=['POST'])
@token_required
def submit_feedback(user, pr_id):
    data = request.get_json()

    if not data or 'comment' not in data or 'approved' not in data:
        return jsonify({
            'success': False,
            'error': 'Comment and approval status are required!'
        }), 400

    db = get_db()
    pr = db.execute('SELECT * FROM pull_requests WHERE id = ?', (pr_id,)).fetchone()

    if not pr:
        return jsonify({
            'success': False,
            'error': 'Pull request not found!'
        }), 404

    # Add feedback
    feedback_id = str(uuid.uuid4())
    db.execute(
        'INSERT INTO feedback (id, pr_id, comment, approved) VALUES (?, ?, ?, ?)',
        (feedback_id, pr_id, data['comment'], 1 if data['approved'] else 0)
    )
    db.commit()

    # If approved, update PR status
    if data['approved']:
        db.execute(
            'UPDATE pull_requests SET status = ? WHERE id = ?',
            ('merged', pr_id)
        )
        db.commit()

    return jsonify({
        'success': True,
        'data': {
            'id': feedback_id,
            'pr_id': pr_id,
            'comment': data['comment'],
            'approved': data['approved'],
            'created_at': datetime.datetime.now().isoformat()
        }
    }), 201

# Chat endpoints
@app.route('/api/chat', methods=['GET'])
@token_required
def get_chat_messages(user):
    reference_id = request.args.get('referenceId')
    reference_type = request.args.get('referenceType')

    db = get_db()

    if reference_id and reference_type:
        messages = db.execute(
            'SELECT * FROM chat_messages WHERE reference_id = ? AND reference_type = ? ORDER BY timestamp ASC',
            (reference_id, reference_type)
        ).fetchall()
    else:
        messages = db.execute(
            'SELECT * FROM chat_messages WHERE reference_id IS NULL ORDER BY timestamp ASC'
        ).fetchall()

    messages_list = []
    for msg in messages:
        messages_list.append({
            'id': msg['id'],
            'sender': msg['sender'],
            'content': msg['content'],
            'reference_id': msg['reference_id'],
            'reference_type': msg['reference_type'],
            'timestamp': msg['timestamp']
        })

    return jsonify({
        'success': True,
        'data': messages_list
    }), 200

@app.route('/api/chat', methods=['POST'])
@token_required
def send_chat_message(user):
    data = request.get_json()

    if not data or 'content' not in data:
        return jsonify({
            'success': False,
            'error': 'Message content is required!'
        }), 400

    # For now, we'll use a simple echo response
    user_message_id = str(uuid.uuid4())
    atim_message_id = str(uuid.uuid4())
    reference_id = data.get('referenceId')
    reference_type = data.get('referenceType')

    db = get_db()

    # Save user message
    db.execute(
        'INSERT INTO chat_messages (id, sender, content, reference_id, reference_type) VALUES (?, ?, ?, ?, ?)',
        (user_message_id, 'user', data['content'], reference_id, reference_type)
    )

    # Generate and save Atim's response (placeholder)
    atim_response = f"This is a placeholder response from Atim. In the actual implementation, this would be generated using an NLP model based on your message: '{data['content']}'"
    db.execute(
        'INSERT INTO chat_messages (id, sender, content, reference_id, reference_type) VALUES (?, ?, ?, ?, ?)',
        (atim_message_id, 'atim', atim_response, reference_id, reference_type)
    )

    db.commit()

    return jsonify({
        'success': True,
        'data': {
            'id': user_message_id,
            'sender': 'user',
            'content': data['content'],
            'reference_id': reference_id,
            'reference_type': reference_type,
            'timestamp': datetime.datetime.now().isoformat()
        }
    }), 201

# Kanban endpoint
@app.route('/api/kanban', methods=['GET'])
def get_kanban_items():
    # For the Kanban view, we can return a public API that doesn't require authentication
    # This will return a mix of Github issues and PRs

    # In a real implementation, we would fetch from the Github API
    # For now, we'll return sample data
    
    items = [
        {
            'id': '1',
            'title': 'Fix supply calculation bug in /chain endpoint',
            'description': 'Currently using chain.size() * 10.0 instead of currentSupply',
            'status': 'todo',
            'type': 'issue',
            'url': 'https://github.com/NiloticNetwork/NiloticNetworkBlockchain/issues/1',
            'number': 1,
            'created_at': '2023-12-15T12:00:00Z',
            'updated_at': '2023-12-15T12:00:00Z'
        },
        {
            'id': '2',
            'title': 'Add getCurrentSupply() method to Blockchain class',
            'description': 'Needed to accurately report the circulating supply of SLW tokens',
            'status': 'in-progress',
            'type': 'pr',
            'url': 'https://github.com/NiloticNetwork/NiloticNetworkBlockchain/pull/2',
            'number': 2,
            'created_at': '2023-12-16T12:00:00Z',
            'updated_at': '2023-12-16T14:00:00Z'
        },
        {
            'id': '3',
            'title': 'Fix race condition in multi-threaded staking',
            'description': 'Adding a mutex to prevent concurrent modifications',
            'status': 'done',
            'type': 'pr',
            'url': 'https://github.com/NiloticNetwork/NiloticNetworkBlockchain/pull/3',
            'number': 3,
            'created_at': '2023-12-10T10:00:00Z',
            'updated_at': '2023-12-11T16:00:00Z'
        },
        {
            'id': '4',
            'title': 'Improve validation for staking amounts',
            'description': 'Add minimum stake amount and better error messages',
            'status': 'in-progress',
            'type': 'issue',
            'url': 'https://github.com/NiloticNetwork/NiloticNetworkBlockchain/issues/4',
            'number': 4,
            'created_at': '2023-12-17T09:00:00Z',
            'updated_at': '2023-12-17T09:00:00Z'
        }
    ]

    return jsonify({
        'success': True,
        'data': items
    }), 200
    
    items = [
        {
            'id': '1',
            'title': 'Fix supply calculation bug in /chain endpoint',
            'description': 'Currently using chain.size() * 10.0 instead of currentSupply',
            'status': 'todo',
            'type': 'issue',
            'url': 'https://github.com/Emmanuel-Odero/nilotic-network/issues/1',
            'number': 1,
            'created_at': '2023-12-15T12:00:00Z',
            'updated_at': '2023-12-15T12:00:00Z'
        },
        {
            'id': '2',
            'title': 'Add getCurrentSupply() method to Blockchain class',
            'description': 'Needed to accurately report the circulating supply of SLW tokens',
            'status': 'in-progress',
            'type': 'pr',
            'url': 'https://github.com/Emmanuel-Odero/nilotic-network/pull/2',
            'number': 2,
            'created_at': '2023-12-16T12:00:00Z',
            'updated_at': '2023-12-16T14:00:00Z'
        },
        {
            'id': '3',
            'title': 'Fix race condition in multi-threaded staking',
            'description': 'Adding a mutex to prevent concurrent modifications',
            'status': 'done',
            'type': 'pr',
            'url': 'https://github.com/Emmanuel-Odero/nilotic-network/pull/3',
            'number': 3,
            'created_at': '2023-12-10T10:00:00Z',
            'updated_at': '2023-12-11T16:00:00Z'
        },
        {
            'id': '4',
            'title': 'Improve validation for staking amounts',
            'description': 'Add minimum stake amount and better error messages',
            'status': 'in-progress',
            'type': 'issue',
            'url': 'https://github.com/Emmanuel-Odero/nilotic-network/issues/4',
            'number': 4,
            'created_at': '2023-12-17T09:00:00Z',
            'updated_at': '2023-12-17T09:00:00Z'
        }
    ]

    return jsonify({
        'success': True,
        'data': items
    }), 200

@app.route('/api/demo/issues', methods=['GET'])
def get_demo_issues():
    # Demo endpoint for issues that doesn't require authentication
    sample_issues = [
        {
            'id': '1',
            'title': 'Incorrect supply calculation in /chain endpoint',
            'description': 'The total supply is incorrectly calculated using chain.size() * 10.0 instead of tracking the actual circulating supply',
            'severity': 'medium',
            'status': 'open',
            'file_path': 'src/core/blockchain.cpp',
            'line_number': 156,
            'suggested_fix': 'Replace with: totalSupply = blockchain.getCurrentSupply();',
            'created_at': '2023-12-15T12:00:00Z',
            'updated_at': '2023-12-15T12:00:00Z'
        },
        {
            'id': '2',
            'title': 'Missing getCurrentSupply() method in Blockchain class',
            'description': 'Need to implement a method to track and return the current supply of SLW tokens',
            'severity': 'medium',
            'status': 'open',
            'file_path': 'src/core/blockchain.h',
            'line_number': 89,
            'suggested_fix': 'Add method: double getCurrentSupply() const;',
            'created_at': '2023-12-16T10:00:00Z',
            'updated_at': '2023-12-16T10:00:00Z'
        },
        {
            'id': '3',
            'title': 'Race condition in multi-threaded staking',
            'description': 'Potential race condition when multiple threads access staking data simultaneously',
            'severity': 'high',
            'status': 'fixed',
            'file_path': 'src/core/staking.cpp',
            'line_number': 234,
            'suggested_fix': 'Add mutex lock around staking operations',
            'created_at': '2023-12-10T09:00:00Z',
            'updated_at': '2023-12-11T16:00:00Z'
        },
        {
            'id': '4',
            'title': 'Improve validation for staking amounts',
            'description': 'Add minimum stake amount and better error messages for invalid staking attempts',
            'severity': 'low',
            'status': 'open',
            'file_path': 'src/core/staking.cpp',
            'line_number': 67,
            'suggested_fix': 'Add validation: if (amount < MIN_STAKE) return error;',
            'created_at': '2023-12-17T14:00:00Z',
            'updated_at': '2023-12-17T14:00:00Z'
        }
    ]
    
    return jsonify({
        'success': True,
        'data': sample_issues
    }), 200

@app.route('/api/demo/chat', methods=['GET'])
def get_demo_chat_messages():
    # Demo endpoint for chat messages that doesn't require authentication
    sample_messages = [
        {
            'id': '1',
            'sender': 'atim',
            'content': 'Hello! I\'m Atim, your AI assistant for the Nilotic Network blockchain. I can help you with code analysis, issue detection, and development questions. What would you like to know?',
            'timestamp': '2023-12-15T10:00:00Z'
        },
        {
            'id': '2',
            'sender': 'user',
            'content': 'Can you help me understand the supply calculation bug?',
            'timestamp': '2023-12-15T10:05:00Z'
        },
        {
            'id': '3',
            'sender': 'atim',
            'content': 'Of course! I detected an issue in the supply calculation. The current code uses `chain.size() * 10.0` which doesn\'t account for the actual circulating supply including premined tokens and block rewards. I\'ve created a pull request to fix this.',
            'timestamp': '2023-12-15T10:06:00Z'
        }
    ]
    
    return jsonify({
        'success': True,
        'data': sample_messages
    }), 200

@app.route('/api/demo/chat', methods=['POST'])
def send_demo_chat_message():
    # Demo endpoint for sending chat messages that doesn't require authentication
    data = request.get_json()
    content = data.get('content', '')
    
    # Simulate Atim's response
    atim_response = {
        'id': str(int(time.time())),
        'sender': 'atim',
        'content': f'I received your message: "{content}". This is a demo response. In a real implementation, I would analyze your question and provide specific insights about the Nilotic Network codebase.',
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'data': atim_response
    }), 200

# GitHub Integration endpoints
@app.route('/api/github/proposals', methods=['GET'])
def get_issue_proposals():
    """Get issue proposals from GitHub analysis"""
    add_log('info', 'GitHub proposals requested', endpoint='/api/github/proposals')
    try:
        github_integration = GitHubIntegration(os.environ.get('GITHUB_TOKEN', ''))
        proposals = github_integration.analyze_repository()
        
        # Convert proposals to dict format
        proposals_data = []
        for proposal in proposals:
            proposal_dict = {
                'id': proposal.id,
                'title': proposal.title,
                'description': proposal.description,
                'severity': proposal.severity,
                'category': proposal.category,
                'file_path': proposal.file_path,
                'line_number': proposal.line_number,
                'suggested_fix': proposal.suggested_fix,
                'labels': proposal.labels,
                'created_at': proposal.created_at,
                'status': proposal.status,
                'github_issue_number': proposal.github_issue_number
            }
            proposals_data.append(proposal_dict)
        
        return jsonify({
            'success': True,
            'data': proposals_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/github/proposals/<proposal_id>/approve', methods=['POST'])
def approve_issue_proposal(proposal_id):
    """Approve an issue proposal and create GitHub issue"""
    add_log('info', f'GitHub issue approval requested for proposal: {proposal_id}', endpoint=f'/api/github/proposals/{proposal_id}/approve')
    
    try:
        # Try Atim's bot token first, fallback to user token
        atim_token = os.environ.get('ATIM_GITHUB_TOKEN', '')
        user_token = os.environ.get('GITHUB_TOKEN', '')
        
        if atim_token:
            add_log('info', 'Using Atim bot token for GitHub operations', endpoint=f'/api/github/proposals/{proposal_id}/approve')
            github_integration = GitHubIntegration()  # Will use ATIM_GITHUB_TOKEN
        else:
            add_log('info', f'Using user token for GitHub operations: {"Set" if user_token else "Not set"}', endpoint=f'/api/github/proposals/{proposal_id}/approve')
            github_integration = GitHubIntegration(user_token)
        
        proposals = github_integration.analyze_repository()
        
        # Find the proposal
        proposal = None
        for p in proposals:
            if p.id == proposal_id:
                proposal = p
                break
        
        if not proposal:
            add_log('warning', f'Proposal not found: {proposal_id}', endpoint=f'/api/github/proposals/{proposal_id}/approve')
            return jsonify({
                'success': False,
                'error': 'Proposal not found'
            }), 404
        
        add_log('info', f'Found proposal: {proposal.title}', endpoint=f'/api/github/proposals/{proposal_id}/approve')
        
        # Create GitHub issue
        issue_number = github_integration.create_github_issue(proposal)
        
        if issue_number:
            proposal.status = 'published'
            proposal.github_issue_number = issue_number
            
            add_log('success', f'GitHub issue created successfully: #{issue_number}', endpoint=f'/api/github/proposals/{proposal_id}/approve')
            
            return jsonify({
                'success': True,
                'data': {
                    'message': f'Issue created successfully with number #{issue_number}',
                    'issue_number': issue_number,
                    'proposal': {
                        'id': proposal.id,
                        'title': proposal.title,
                        'status': proposal.status,
                        'github_issue_number': proposal.github_issue_number
                    }
                }
            }), 200
        else:
            add_log('error', f'Failed to create GitHub issue for proposal: {proposal_id}', endpoint=f'/api/github/proposals/{proposal_id}/approve')
            return jsonify({
                'success': False,
                'error': 'Failed to create GitHub issue. Check server logs for details.'
            }), 500
            
    except Exception as e:
        add_log('error', f'Exception in approve_issue_proposal: {str(e)}', endpoint=f'/api/github/proposals/{proposal_id}/approve')
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/github/proposals/<proposal_id>/reject', methods=['POST'])
def reject_issue_proposal(proposal_id):
    """Reject an issue proposal"""
    try:
        github_integration = GitHubIntegration(os.environ.get('GITHUB_TOKEN', ''))
        proposals = github_integration.analyze_repository()
        
        # Find the proposal
        proposal = None
        for p in proposals:
            if p.id == proposal_id:
                proposal = p
                break
        
        if not proposal:
            return jsonify({
                'success': False,
                'error': 'Proposal not found'
            }), 404
        
        proposal.status = 'rejected'
        
        return jsonify({
            'success': True,
            'data': {
                'message': 'Proposal rejected successfully',
                'proposal': {
                    'id': proposal.id,
                    'title': proposal.title,
                    'status': proposal.status
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/github/stats', methods=['GET'])
def get_github_stats():
    """Get GitHub repository statistics"""
    try:
        github_integration = GitHubIntegration(os.environ.get('GITHUB_TOKEN', ''))
        stats = github_integration.get_repository_stats()
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5070)
