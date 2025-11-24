# save this as seed.py in your project root folder
# run: python seed.py

from app import create_app, db
from app.models import User, Post, PostLike, Follow, Role
from datetime import datetime, timedelta

def seed_database():
    """Додає тестові дані до бази"""
    
    app = create_app('development')  # або твій конфіг
    
    with app.app_context():
        # 1. Видалити старі дані (опціонально)
        print("🗑️ Очищуємо старі дані...")
        db.drop_all()
        db.create_all()
        
        # 2. Створити ролі
        print("👤 Створюємо ролі...")
        Role.insert_roles()
        
        # 3. Створити користувачів
        print("👥 Створюємо користувачів...")
        
        user1 = User(
            email='blackjack@example.com',
            username='blackjack',
            user_image_url='https://i.pravatar.cc/150?img=1',
            is_active=True,
            role_id=1  # User
        )
        user1.password = 'password123'
        
        user2 = User(
            email='hookers@example.com',
            username='hookers',
            user_image_url='https://i.pravatar.cc/150?img=2',
            is_active=True,
            role_id=2  # Moderator
        )
        user2.password = 'password123'
        
        user3 = User(
            email='themepark@example.com',
            username='themepark',
            user_image_url='https://i.pravatar.cc/150?img=3',
            is_active=True,
            role_id=3
        )
        user3.password = 'password123'
        
        db.session.add_all([user1, user2, user3])
        db.session.commit()
        print(f"Створено 3 користувачів: themepark, blackjack and hookers")
        
        # 4. Створити Follow (кисло та боб слідять за алісою)
        print("🔗 Додаємо підписки...")
        
        follow1 = Follow(follower_id=user2.id, following_to=user1.id)  # hookers follows blackjack
        follow2 = Follow(follower_id=user3.id, following_to=user1.id)  # themepark follows blackjack
        follow3 = Follow(follower_id=user1.id, following_to=user2.id)  # blackjack follows hookers
        
        db.session.add_all([follow1, follow2, follow3])
        db.session.commit()
        print(f"✅ hookers та themepark тепер слідять за blackjack")
        print(f"✅ blackjack тепер слідить за hookers")
        
        # 5. Створити пости
        print("📝 Створюємо пости...")
        
        now = datetime.utcnow()
        
        # blackjack's posts
        post1 = Post(
            body='Hello! This is my first post! 👋',
            uploaded_content_url='https://via.placeholder.com/500x500?text=blackjack+Post+1',
            author_id=user1.id,
            timestamp=now - timedelta(hours=3)
        )
        
        post2 = Post(
            body='Beautiful sunset today! 🌅 Nature is amazing!',
            uploaded_content_url='https://via.placeholder.com/500x500?text=Sunset',
            author_id=user1.id,
            timestamp=now - timedelta(hours=2)
        )
        
        post3 = Post(
            body='Just finished a great book! Highly recommend it to everyone 📚',
            uploaded_content_url='https://via.placeholder.com/500x500?text=Book',
            author_id=user1.id,
            timestamp=now - timedelta(hours=1)
        )
        
        # hookers's posts
        post4 = Post(
            body='Coding all day! 💻 Love what I do',
            uploaded_content_url='https://via.placeholder.com/500x500?text=hookers+Code',
            author_id=user2.id,
            timestamp=now - timedelta(hours=4)
        )
        
        post5 = Post(
            body='Coffee time! ☕ Best part of the day',
            uploaded_content_url='https://via.placeholder.com/500x500?text=Coffee',
            author_id=user2.id,
            timestamp=now - timedelta(hours=2)
        )
        
        post6 = Post(
            body='Working out at the gym 💪 Stay healthy!',
            uploaded_content_url='https://via.placeholder.com/500x500?text=Gym',
            author_id=user2.id,
            timestamp=now - timedelta(minutes=30)
        )
        
        # themepark's posts
        post7 = Post(
            body='Just traveled to a new city! 🗽 Amazing experience!',
            uploaded_content_url='https://via.placeholder.com/500x500?text=Travel',
            author_id=user3.id,
            timestamp=now - timedelta(hours=5)
        )
        
        post8 = Post(
            body='Cooking dinner for my family 🍝 Delicious!',
            uploaded_content_url='https://via.placeholder.com/500x500?text=Cooking',
            author_id=user3.id,
            timestamp=now - timedelta(hours=1)
        )
        
        post9 = Post(
            body='Movie night with friends! 🎬 Popcorn time!',
            uploaded_content_url='https://via.placeholder.com/500x500?text=Movie',
            author_id=user3.id,
            timestamp=now - timedelta(minutes=15)
        )
        
        db.session.add_all([post1, post2, post3, post4, post5, post6, post7, post8, post9])
        db.session.commit()
        print(f"✅ Створено 9 постів (3 на кожного користувача)")
        
        # 6. Додати лайки
        print("❤️ Додаємо лайки...")
        
        # hookers likes blackjack's posts
        like1 = PostLike(user_id=user2.id, post_id=post1.id)
        like2 = PostLike(user_id=user2.id, post_id=post2.id)
        
        # themepark likes blackjack's posts
        like3 = PostLike(user_id=user3.id, post_id=post1.id)
        like4 = PostLike(user_id=user3.id, post_id=post3.id)
        
        # blackjack likes hookers's posts
        like5 = PostLike(user_id=user1.id, post_id=post4.id)
        like6 = PostLike(user_id=user1.id, post_id=post6.id)
        
        # blackjack likes themepark's posts
        like7 = PostLike(user_id=user1.id, post_id=post7.id)
        like8 = PostLike(user_id=user1.id, post_id=post8.id)
        
        # hookers likes themepark's posts
        like9 = PostLike(user_id=user2.id, post_id=post9.id)
        
        db.session.add_all([like1, like2, like3, like4, like5, like6, like7, like8, like9])
        db.session.commit()
        print(f"✅ Додано 9 лайків")
        
        # 7. Вивести статистику
        print("\n" + "="*50)
        print("📊 СТАТИСТИКА ТЕСТОВИХ ДАНИХ")
        print("="*50)
        
        all_users = User.query.all()
        all_posts = Post.query.all()
        all_likes = PostLike.query.all()
        all_follows = Follow.query.all()
        
        print(f"👥 Користувачів: {len(all_users)}")
        print(f"📝 Постів: {len(all_posts)}")
        print(f"❤️ Лайків: {len(all_likes)}")
        print(f"🔗 Підписок: {len(all_follows)}")
        
        print("\n👤 КОРИСТУВАЧІ:")
        for user in all_users:
            followers_count = user.got_followed_back_list.count()
            following_count = user.following_to_list.count()
            posts_count = user.posts.count()
            print(f"  - {user.username} (email: {user.email})")
            print(f"    Слідків: {following_count}, Послідовників: {followers_count}, Постів: {posts_count}")
        
        print("\n" + "="*50)
        print("✅ БАЗА ДАНИХ УСПІШНО ЗАПОВНЕНА!")
        print("="*50)
        print("\nДля входу використай:")
        print("  Username: blackjack, Password: password123")
        print("  Username: hookers,   Password: password123")
        print("  Username: themepark, Password: password123")

if __name__ == '__main__':
    seed_database()