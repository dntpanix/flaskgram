"""
Instagram DOM Emulator для автоматизованого тестування
Емулює структуру DOM Instagram з мінімальними запитами до API
"""

from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Симуляція бази даних (в продакшені використовуйте реальну БД)
MOCK_DATA = {
    'user': {
        'username': 'testuser',
        'full_name': 'Test User',
        'profile_pic': 'https://via.placeholder.com/150',
        'bio': 'Test bio for automation',
        'followers': 1234,
        'following': 567,
        'posts_count': 42
    },
    'posts': [
        {
            'id': f'post_{i}',
            'image_url': f'https://via.placeholder.com/600x600?text=Post+{i}',
            'caption': f'Test caption for post {i}',
            'likes': 100 + i * 10,
            'comments_count': 5 + i,
            'timestamp': '2024-01-15T12:00:00Z',
            'location': 'Test Location' if i % 2 == 0 else None
        }
        for i in range(1, 13)
    ],
    'stories': [
        {
            'id': f'story_{i}',
            'image_url': f'https://via.placeholder.com/400x700?text=Story+{i}',
            'timestamp': '2024-01-15T10:00:00Z'
        }
        for i in range(1, 5)
    ]
}

@app.route('/')
def index():
    """Головна сторінка - стрічка новин"""
    return render_template('feed.html', posts=MOCK_DATA['posts'])

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
    user_data = MOCK_DATA['user'].copy()
    user_data['username'] = username
    return render_template('profile.html', user=user_data, posts=MOCK_DATA['posts'])

@app.route('/api/posts/<post_id>/like', methods=['POST'])
def like_post(post_id):
    """API для лайку поста"""
    # Симуляція лайку
    for post in MOCK_DATA['posts']:
        if post['id'] == post_id:
            post['likes'] += 1
            return jsonify({'success': True, 'likes': post['likes']})
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
    return jsonify({'stories': MOCK_DATA['stories']})

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
    return render_template('explore.html', posts=MOCK_DATA['posts'])

# ============= HTML Templates =============
# Створіть папку templates/ і додайте наступні файли:

if __name__ == '__main__':
    # Створення необхідних директорій
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Створення базового шаблону
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Instagram{% endblock %}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #fafafa; }
        
        /* Header */
        .header { background: white; border-bottom: 1px solid #dbdbdb; padding: 10px 0; position: fixed; width: 100%; top: 0; z-index: 100; }
        .header-content { max-width: 975px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; }
        .logo { font-family: 'Courier New', monospace; font-size: 24px; font-weight: bold; }
        .search-bar { background: #efefef; border: 1px solid #dbdbdb; border-radius: 3px; padding: 5px 10px; width: 250px; }
        .nav-icons { display: flex; gap: 20px; }
        .nav-icon { font-size: 24px; cursor: pointer; text-decoration: none; color: black; }
        
        /* Main Content */
        .main-content { max-width: 975px; margin: 80px auto 0; padding: 20px; }
        
        /* Post Card */
        .post-card { background: white; border: 1px solid #dbdbdb; border-radius: 3px; margin-bottom: 20px; }
        .post-header { display: flex; align-items: center; padding: 14px; border-bottom: 1px solid #efefef; }
        .post-avatar { width: 32px; height: 32px; border-radius: 50%; background: #ccc; margin-right: 10px; }
        .post-username { font-weight: 600; font-size: 14px; }
        .post-image { width: 100%; display: block; }
        .post-actions { padding: 14px; }
        .action-buttons { display: flex; gap: 15px; margin-bottom: 10px; }
        .action-btn { background: none; border: none; font-size: 24px; cursor: pointer; }
        .post-likes { font-weight: 600; font-size: 14px; margin-bottom: 8px; }
        .post-caption { font-size: 14px; }
        .post-caption .username { font-weight: 600; margin-right: 5px; }
        .post-comments { color: #8e8e8e; font-size: 14px; margin-top: 5px; cursor: pointer; }
        .comment-input { width: 100%; border: none; outline: none; padding: 10px 0; border-top: 1px solid #efefef; }
        
        /* Profile */
        .profile-header { display: flex; gap: 30px; padding: 30px 0; border-bottom: 1px solid #dbdbdb; margin-bottom: 30px; }
        .profile-avatar { width: 150px; height: 150px; border-radius: 50%; background: #ccc; }
        .profile-info { flex: 1; }
        .profile-username { font-size: 28px; font-weight: 300; margin-bottom: 20px; }
        .profile-stats { display: flex; gap: 40px; margin-bottom: 20px; }
        .stat { font-size: 16px; }
        .stat-value { font-weight: 600; }
        .profile-bio { font-size: 14px; }
        .follow-btn { background: #0095f6; color: white; border: none; padding: 8px 24px; border-radius: 4px; font-weight: 600; cursor: pointer; }
        
        /* Grid */
        .posts-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; }
        .grid-post { aspect-ratio: 1; background: #ccc; cursor: pointer; position: relative; }
        .grid-post img { width: 100%; height: 100%; object-fit: cover; }
        
        /* Login */
        .login-container { max-width: 350px; margin: 50px auto; }
        .login-box { background: white; border: 1px solid #dbdbdb; padding: 40px; text-align: center; }
        .login-logo { font-size: 48px; margin-bottom: 30px; }
        .login-input { width: 100%; padding: 9px 8px; border: 1px solid #dbdbdb; border-radius: 3px; margin-bottom: 8px; background: #fafafa; }
        .login-btn { width: 100%; background: #0095f6; color: white; border: none; padding: 8px; border-radius: 8px; font-weight: 600; cursor: pointer; margin-top: 10px; }
    </style>
</head>
<body>
    {% block header %}
    <header class="header">
        <div class="header-content">
            <div class="logo">Instagram</div>
            <input type="text" class="search-bar" placeholder="Пошук" id="search-input">
            <div class="nav-icons">
                <a href="/" class="nav-icon" id="home-icon">🏠</a>
                <a href="/direct/inbox/" class="nav-icon" id="direct-icon">✉️</a>
                <a href="/explore/" class="nav-icon" id="explore-icon">🔍</a>
                <a href="/profile/testuser" class="nav-icon" id="profile-icon">👤</a>
            </div>
        </div>
    </header>
    {% endblock %}
    
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>
    
    <script>
        {% block scripts %}{% endblock %}
    </script>
</body>
</html>''')
    
    # Шаблон стрічки
    with open('templates/feed.html', 'w', encoding='utf-8') as f:
        f.write('''{% extends "base.html" %}
{% block content %}
<div class="feed-container">
    {% for post in posts %}
    <article class="post-card" data-post-id="{{ post.id }}">
        <div class="post-header">
            <div class="post-avatar"></div>
            <span class="post-username">testuser</span>
        </div>
        <img src="{{ post.image_url }}" alt="Post image" class="post-image">
        <div class="post-actions">
            <div class="action-buttons">
                <button class="action-btn like-btn" data-post-id="{{ post.id }}">❤️</button>
                <button class="action-btn comment-btn">💬</button>
                <button class="action-btn share-btn">📤</button>
            </div>
            <div class="post-likes" data-likes="{{ post.likes }}">
                <span class="likes-count">{{ post.likes }}</span> вподобань
            </div>
            <div class="post-caption">
                <span class="username">testuser</span>
                {{ post.caption }}
            </div>
            <div class="post-comments">
                Переглянути всі коментарі ({{ post.comments_count }})
            </div>
            <input type="text" class="comment-input" placeholder="Додати коментар..." data-post-id="{{ post.id }}">
        </div>
    </article>
    {% endfor %}
</div>

<script>
document.querySelectorAll('.like-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const postId = this.dataset.postId;
        fetch(`/api/posts/${postId}/like`, { method: 'POST' })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    const likesEl = document.querySelector(`[data-post-id="${postId}"] .likes-count`);
                    likesEl.textContent = data.likes;
                }
            });
    });
});

document.querySelectorAll('.comment-input').forEach(input => {
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && this.value.trim()) {
            const postId = this.dataset.postId;
            fetch(`/api/posts/${postId}/comment`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ comment: this.value })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    this.value = '';
                    alert('Коментар додано!');
                }
            });
        }
    });
});
</script>
{% endblock %}''')
    
    # Шаблон логіну
    with open('templates/login.html', 'w', encoding='utf-8') as f:
        f.write('''{% extends "base.html" %}
{% block header %}{% endblock %}
{% block content %}
<div class="login-container">
    <div class="login-box">
        <div class="login-logo">Instagram</div>
        <form id="login-form">
            <input type="text" name="username" class="login-input" placeholder="Телефон, ім'я користувача або ел. адреса" id="username-input" required>
            <input type="password" name="password" class="login-input" placeholder="Пароль" id="password-input" required>
            <button type="submit" class="login-btn" id="login-btn">Увійти</button>
        </form>
    </div>
</div>

<script>
document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    fetch('/login', {
        method: 'POST',
        body: formData
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect;
        } else {
            alert(data.error);
        }
    });
});
</script>
{% endblock %}''')
    
    # Шаблон профілю
    with open('templates/profile.html', 'w', encoding='utf-8') as f:
        f.write('''{% extends "base.html" %}
{% block content %}
<div class="profile-header">
    <div class="profile-avatar"></div>
    <div class="profile-info">
        <div class="profile-username">{{ user.username }}</div>
        <div class="profile-stats">
            <span class="stat"><span class="stat-value">{{ user.posts_count }}</span> публікацій</span>
            <span class="stat"><span class="stat-value">{{ user.followers }}</span> підписників</span>
            <span class="stat"><span class="stat-value">{{ user.following }}</span> підписок</span>
        </div>
        <div class="profile-bio">{{ user.bio }}</div>
        <button class="follow-btn" id="follow-btn">Підписатися</button>
    </div>
</div>

<div class="posts-grid">
    {% for post in posts %}
    <div class="grid-post" data-post-id="{{ post.id }}">
        <img src="{{ post.image_url }}" alt="Post">
    </div>
    {% endfor %}
</div>

<script>
document.getElementById('follow-btn').addEventListener('click', function() {
    fetch('/api/user/{{ user.username }}/follow', { method: 'POST' })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                this.textContent = 'Відписатися';
            }
        });
});
</script>
{% endblock %}''')
    
    # Додаткові шаблони
    with open('templates/direct.html', 'w', encoding='utf-8') as f:
        f.write('''{% extends "base.html" %}
{% block content %}
<h2>Direct Messages</h2>
<div class="messages-list">
    {% for msg in messages %}
    <div class="message-item" data-message-id="{{ msg.id }}">
        <strong>{{ msg.username }}</strong>: {{ msg.last_message }}
    </div>
    {% endfor %}
</div>
{% endblock %}''')
    
    with open('templates/explore.html', 'w', encoding='utf-8') as f:
        f.write('''{% extends "base.html" %}
{% block content %}
<h2>Explore</h2>
<div class="posts-grid">
    {% for post in posts %}
    <div class="grid-post" data-post-id="{{ post.id }}">
        <img src="{{ post.image_url }}" alt="Post">
    </div>
    {% endfor %}
</div>
{% endblock %}''')
    
    print("✅ Шаблони створено успішно!")
    print("🚀 Запуск сервера на http://localhost:5000")
    print("\nДоступні сторінки:")
    print("  - / (стрічка)")
    print("  - /login (авторизація)")
    print("  - /profile/testuser (профіль)")
    print("  - /direct/inbox/ (повідомлення)")
    print("  - /explore/ (пошук)")
    
    app.run(debug=True, port=5000)