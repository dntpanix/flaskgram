import datetime
from flask import (
    Flask, 
    render_template, 
    request, 
    jsonify, 
    session
)

from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    # jwt = JWTManager(app)
    jwt.init_app(app)

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

    @app.route('/')
    def index():
        """Головна сторінка - стрічка новин"""
        return render_template('feed.html')#, posts=MOCK_DATA['posts']

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Сторінка логіну"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Тут можна додати реальну авторизацію через Instagram API
            # Для тестування просто зберігаємо сесію
            if username and password:
                session['logged_in'] = True
                session['username'] = username
                return jsonify({'success': True, 'redirect': '/'})
            
            return jsonify({'success': False, 'error': 'Invalid credentials'})
        
        return render_template('login.html')

    @app.route('/profile/<username>')
    def profile(username):
        """Сторінка профілю користувача"""
        # user_data = MOCK_DATA['user'].copy()
        # user_data['username'] = username
        return render_template('profile.html')#, user=user_data, posts=MOCK_DATA['posts']

    @app.route('/api/posts/<post_id>/like', methods=['POST'])
    def like_post(post_id):
        """API для лайку поста"""
        # Симуляція лайку
        # for post in MOCK_DATA['posts']:
        #     if post['id'] == post_id:
        #         post['likes'] += 1
        #         return jsonify({'success': True, 'likes': post['likes']})
        return jsonify({'success': False}), 404

    @app.route('/api/posts/<post_id>/comment', methods=['POST'])
    def comment_post(post_id):
        """API для коментування"""
        comment_text = request.json.get('comment')
        if comment_text:
            return jsonify({
                'success': True,
                'comment': {
                    'id': f'comment_{datetime.now().timestamp()}',
                    'text': comment_text,
                    'username': session.get('username', 'testuser'),
                    'timestamp': datetime.now().isoformat()
                }
            })
        return jsonify({'success': False}), 400

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
