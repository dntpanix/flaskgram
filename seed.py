# save this as seed.py in your project root folder
# run: python seed.py

from app import create_app, db
from app.models import User, Post, PostLike, Follow, Role
from datetime import datetime, timedelta

def seed_database():
    """Adds test data to the database"""
    
    app = create_app('development')  # або твій конфіг
    
    with app.app_context():
        # 1. Видалити старі дані (опціонально)
        print("🗑️ Clearing old data...")
        db.drop_all()
        db.create_all()
        
        # 2. Створити ролі
        print("👤 Creating roles...")
        Role.insert_roles()
        
        # 3. Створити користувачів
        print("👥 Creating users...")
        
        user1 = User(
            email='blackjack@example.com',
            username='blackjack',
            user_image_url='https://i.pravatar.cc/150?img=10',
            is_active=True,
            role_id=1  # User
        )
        user1.password = 'password123'
        
        user2 = User(
            email='hookers@example.com',
            username='hookers',
            user_image_url='https://i.pravatar.cc/150?img=5',
            is_active=True,
            role_id=2  # Moderator
        )
        user2.password = 'password123'
        
        user3 = User(
            email='themepark@example.com',
            username='themepark',
            user_image_url='https://i.pravatar.cc/150?img=3',
            is_active=True,
            role_id=3 # Administrator
        )
        user3.password = 'password123'
        
        db.session.add_all([user1, user2, user3])
        db.session.commit()
        print(f"Created 3 users: {user3.username}, {user1.username} and {user2.username}")
        
        # 4. Створити Follow (кисло та боб слідять за алісою)
        print("🔗 Adding followers...")
        
        follow1 = Follow(follower_id=user2.id, following_to=user1.id)  # hookers follows blackjack
        follow2 = Follow(follower_id=user3.id, following_to=user1.id)  # themepark follows blackjack
        follow3 = Follow(follower_id=user1.id, following_to=user2.id)  # blackjack follows hookers
        
        db.session.add_all([follow1, follow2, follow3])
        db.session.commit()
        print(f"✅ hookers and themepark are now following blackjack")
        print(f"✅ blackjack is now following hookers")
        
        # 5. Створити пости
        print("📝 Creating posts...")
        
        now = datetime.utcnow()
        
        # blackjack's posts
        post1 = Post(
            body='Hello! This is my first post! 👋',
            uploaded_content_url='https://placehold.co/500x500?text=blackjack+Post+1',
            author_id=user1.id,
            timestamp=now - timedelta(hours=3)
        )
        
        post2 = Post(
            body='Beautiful sunset today! 🌅 Nature is amazing!',
            uploaded_content_url='https://placehold.co/500x500?text=Sunset',
            author_id=user1.id,
            timestamp=now - timedelta(hours=2)
        )
        
        post3 = Post(
            body='Just finished a great book! Highly recommend it to everyone 📚',
            uploaded_content_url='https://placehold.co/500x500?text=Book',
            author_id=user1.id,
            timestamp=now - timedelta(hours=1)
        )
        
        # hookers's posts
        post4 = Post(
            body='Coding all day! 💻 Love what I do',
            uploaded_content_url='https://placehold.co/500x500?text=hookers+Code',
            author_id=user2.id,
            timestamp=now - timedelta(hours=4)
        )
        
        post5 = Post(
            body='Coffee time! ☕ Best part of the day',
            uploaded_content_url='https://placehold.co/500x500?text=Coffee',
            author_id=user2.id,
            timestamp=now - timedelta(hours=2)
        )
        
        post6 = Post(
            body='Working out at the gym 💪 Stay healthy!',
            uploaded_content_url='https://placehold.co/500x500?text=Gym',
            author_id=user2.id,
            timestamp=now - timedelta(minutes=30)
        )
        
        # themepark's posts
        post7 = Post(
            body='Just traveled to a new city! 🗽 Amazing experience!',
            uploaded_content_url='https://placehold.co/500x500?text=Travel',
            author_id=user3.id,
            timestamp=now - timedelta(hours=5)
        )
        
        post8 = Post(
            body='Cooking dinner for my family 🍝 Delicious!',
            uploaded_content_url='https://placehold.co/500x500?text=Cooking',
            author_id=user3.id,
            timestamp=now - timedelta(hours=1)
        )
        
        post9 = Post(
            body='Movie night with friends! 🎬 Popcorn time!',
            uploaded_content_url='https://placehold.co/500x500?text=Movie',
            author_id=user3.id,
            timestamp=now - timedelta(minutes=15)
        )
        
        db.session.add_all([post1, post2, post3, post4, post5, post6, post7, post8, post9])
        db.session.commit()
        print(f"✅ Created 9 post (3 per user)")
        
        # 6. Додати лайки
        print("❤️ Adding likes...")
        
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
        print(f"✅ Added 9 likes")
        
        # 7. Вивести статистику
        print("\n" + "="*50)
        print("📊 TEST DATA STATISTICS")
        print("="*50)
        
        all_users = User.query.all()
        all_posts = Post.query.all()
        all_likes = PostLike.query.all()
        all_follows = Follow.query.all()
        
        print(f"👥 Users: {len(all_users)}")
        print(f"📝 Posts: {len(all_posts)}")
        print(f"❤️ Likes: {len(all_likes)}")
        print(f"🔗 Follows: {len(all_follows)}")

        
        print("\n👤 USERS:")
        for user in all_users:
            followers_count = user.got_followed_back_list.count()
            following_count = user.following_to_list.count()
            posts_count = user.posts.count()
            print(f"  - {user.username} (email: {user.email})")
            print(f"    Following: {following_count}, Followers: {followers_count}, Posts: {posts_count}")
        
        print("\n" + "="*50)
        print("✅ DATABASE SUCCESSFULLY SEEDED!")
        print("="*50)

        print("\nTo log in, use:")
        print("  Username: blackjack, Password: password123")
        print("  Username: hookers,   Password: password123")
        print("  Username: themepark, Password: password123")


if __name__ == '__main__':
    seed_database()
