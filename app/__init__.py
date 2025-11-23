import datetime
from flask import Flask, render_template, request, jsonify, session, send_from_directory #redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

import os

db = SQLAlchemy()
jwt = JWTManager()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    # якщо потрібно, можна вказати view у blueprint: 'auth.login'
    login_manager.login_view = 'login' 

    from .postRoute import postRoute as postRouteBlueprint
    app.register_blueprint(postRouteBlueprint) 

    from .authRoute import authRoute as authRouteBlueprint
    app.register_blueprint(authRouteBlueprint)

    from .userRoute import userRoute as userRouteBlueprint
    app.register_blueprint(userRouteBlueprint)

    from .msgRoute import msgRoute as msgRouteBlueprint
    app.register_blueprint(msgRouteBlueprint)

    from .likesRoute import likesRoute as likesRouteBlueprint
    app.register_blueprint(likesRouteBlueprint)

    # --- user_loader для flask-login ---
    from .models import User
    from .models import Post

    def get_posts_for_feed():
        # якщо в тебе є модель Post — використовуй її
        try:
            from .models import Post
            posts = Post.query.order_by(Post.created_at.desc()).all()
            return posts
        except Exception:
            # fallback: пустий список
            return []
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                'images/favicon.png', mimetype='image/vnd.microsoft.icon')

    @app.route('/')
    @login_required
    def index():
        """Головна сторінка - стрічка новин"""
        posts = get_posts_for_feed()
        # передаємо posts у шаблон, щоб UI використовував дані з API/бази
        return render_template('feed.html', posts=posts)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Сторінка логіну"""
        if request.method == 'POST':
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'error': "Unsupported Media Type. Content-Type must be 'application/json'"
                }), 415

            data = request.get_json(silent=True)
            if not data:
                return jsonify({'success': False, 'error': 'Invalid JSON body'}), 400

            username = data.get('username', '').strip()
            password = data.get('password', '')

            if not username or not password:
                return jsonify({'success': False, 'error': 'Missing username or password'}), 400

            # --- Якщо у вас CSRF захист (Flask-WTF) і ви чекаєте токен в заголовку: ---
            # try:
            #     csrf_token = request.headers.get('X-CSRFToken') or request.headers.get('X-CSRF-Token')
            #     if csrf_token:
            #         validate_csrf(csrf_token)
            # except CSRFError as e:
            #     return jsonify({'success': False, 'error': 'Invalid CSRF token'}), 400

            # --- Аутентифікація ---
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)  # створює flask-login сесію
                # можеш повертати токен для API, якщо потрібно
                return jsonify({'success': True, 'redirect': '/'})
            else:
                return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        
        return render_template('login.html')

    @app.route('/profile/<username>')
    def profile(username):
        """Сторінка профілю користувача"""
        # отримуємо дані профілю з БД (приклад)
        user = User.query.filter_by(username=username).first()
        if not user:
            return render_template('profile.html', user=None), 404

        # приклад: отримати пости користувача
        try:
            from .models import Post
            posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
        except Exception:
            posts = []
        return render_template('profile.html', user=user, posts=posts)

    # Приклади API-ендпоінтів (заміни на свої blueprints якщо вони вже є)
    @app.route('/api/posts/<post_id>/like', methods=['POST'])
    @jwt_required(optional=True)  # або required=True — залежить від бажаного захисту
    def like_post(post_id):
        # Тут логіка лайка: знайти пост, додати лайк, зберегти
        from .models import Like
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            return jsonify({'success': False}), 404
        # приклад: додати лайк
        # current_user може бути доступний через flask-login або через JWT identity
        identity = None
        try:
            identity = get_jwt_identity()
        except Exception:
            identity = current_user.get_id() if current_user.is_authenticated else None
        # ... логіка створення Like ...
        post.likes_count = (post.likes_count or 0) + 1
        db.session.commit()
        return jsonify({'success': True, 'likes': post.likes_count})

    @app.route('/api/posts/<post_id>/comment', methods=['POST'])
    @jwt_required(optional=True)
    def comment_post(post_id):
        comment_text = request.json.get('comment')
        if not comment_text:
            return jsonify({'success': False}), 400
        from .models import Post, Comment
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            return jsonify({'success': False}), 404
        user_identity = get_jwt_identity() or (current_user.get_id() if current_user.is_authenticated else None)
        username_for_comment = 'anonymous'
        if user_identity:
            u = User.query.get(user_identity)
            if u:
                username_for_comment = u.username
        comment = Comment(post_id=post.id, text=comment_text, username=username_for_comment, timestamp=datetime.datetime.utcnow())
        db.session.add(comment)
        db.session.commit()
        return jsonify({'success': True, 'comment': {
            'id': comment.id,
            'text': comment.text,
            'username': comment.username,
            'timestamp': comment.timestamp.isoformat()
        }})

    @app.route('/api/user/<username>/follow', methods=['POST'])
    def follow_user(username):
        """API для підписки на користувача"""
        return jsonify({'success': True, 'following': True})

    @app.route('/api/stories')
    def get_stories():
        """API для отримання stories"""
        return jsonify({'stories': 'stories'})

    @app.route('/direct/inbox/')
    def direct_inbox():
        """Сторінка Direct Messages"""
        messages = [
            {
                'id': 'msg_1',
                'username': 'friend1',
                'last_message': 'Hey, how are you?',
                'timestamp': '5m ago',
                'unread': True
            },
            {
                'id': 'msg_2',
                'username': 'friend2',
                'last_message': 'Check this out!',
                'timestamp': '1h ago',
                'unread': False
            }
        ]
        return render_template('direct.html', messages=messages)

    @app.route('/explore/')
    def explore():
        """Сторінка Explore"""
        return render_template('explore.html')#, posts=MOCK_DATA['posts']

    return app
