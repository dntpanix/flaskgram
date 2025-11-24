from datetime import timedelta
from app.postRoute.errors import bad_request, custom404, unauthorized
from . import authRoute
from flask import request, jsonify, current_app, render_template, redirect
from ..models import User, TokenBlocklist
from datetime import datetime
from datetime import timezone

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, current_user as jwt_user
from flask_jwt_extended import decode_token, get_jwt
from flask_login import login_user, logout_user, current_user
from .. import db


@authRoute.route('/login', methods=['GET', 'POST'])
def login():
    """Login endpoint - використовує Flask-Login сесії"""
    # Якщо вже залогінений
    if current_user.is_authenticated:
        return redirect('/')
    
    # GET - повертаємо HTML форму
    if request.method == 'GET':
        return render_template('login.html')
    
    # POST - обробляємо логін
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': "Content-Type must be 'application/json'"
        }), 415

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'error': 'Invalid JSON'}), 400
    
    email = None
    username = None
    user_login = data.get('username')
    if "@" in user_login and "." in user_login:
        email = user_login.strip().lower()
    else:
        username = user_login.strip().lower()
    password = data.get('password', '')

    print(f"🔐 Спроба логіну: email={email}, username={username}")

    # Шукаємо користувача
    user = None
    if email:
        user = User.query.filter_by(email=email).first()
    elif username:
        user = User.query.filter_by(username=username).first()
    
    if user and user.verify_password(password):
        # ✅ Успішна аутентифікація
        print(f"✅ Користувач {user.username} залогінився")
        
        return jsonify({
            'success': True,
            'redirect': '/',
            'user_id': user.id,
            'username': user.username,
            'message': 'Login successful!'
        }), 200
    else:
        print(f"❌ Невдала спроба логіну")
        return jsonify({
            'success': False, 
            'error': 'Invalid credentials'
        }), 401


@authRoute.route('/register', methods=['GET', 'POST'])
def register():
    """Register endpoint"""
    if current_user.is_authenticated:
        return redirect('/')
    
    if request.method == 'GET':
        return render_template('signup.html')
    
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 415

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'error': 'Invalid JSON'}), 400

    email = data.get('email', '').strip().lower()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    password_confirm = data.get('password_confirm', '')

    print(f"📝 Спроба реєстрації: {email}, {username}")

    # Валідація
    if not email or not username or not password:
        return jsonify({'success': False, 'error': 'Fill all fields'}), 400

    if len(username) < 3:
        return jsonify({'success': False, 'error': 'Username must be at least 3 characters'}), 400

    if len(password) < 6:
        return jsonify({'success': False, 'error': 'Password must be at least 6 characters'}), 400

    if password != password_confirm:
        return jsonify({'success': False, 'error': 'Passwords do not match'}), 400

    # Перевіряємо чи існує
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'error': 'Email already registered'}), 409

    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'error': 'Username already taken'}), 409

    # Створюємо користувача
    try:
        new_user = User(email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        print(f"✅ Новий користувач: {username}")
        
        return jsonify({
            'success': True,
            'message': 'Registration successful! Redirecting to login...',
            'redirect': '/login'
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"❌ Помилка реєстрації: {str(e)}")
        return jsonify({'success': False, 'error': f'Error: {str(e)}'}), 500


@authRoute.route('/logout', methods=['GET'])
def logout():
    """Logout endpoint"""
    if current_user.is_authenticated:
        username = current_user.username
        logout_user()
        print(f"✅ Користувач {username} вийшов")
        return jsonify({'success': True, 'message': 'Logged out'})
    
    return redirect('/login')


@authRoute.route('/update-password', methods=['POST'])
@jwt_required()
def update_passwords():
    """Оновлення паролю (JWT захищено)"""
    user = User.query.get(jwt_user.id)
    old_password = request.json.get('old_password', None)
    new_password = request.json.get('new_password', None)

    if not user:
        return custom404("User not found.")
    
    elif not user.verify_password(old_password):
        return unauthorized("Incorrect old password")
    
    else:        
        user.password = new_password
        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "Password Updated."}), 200