from dotenv import load_dotenv
from app import create_app, db
from flask_migrate import Migrate
from app.models import Follow, PostLike, Role, TokenBlocklist, User, Post, Comment, Message


load_dotenv()

# using default config
_cached_app = None

def create_or_get_app(config_name='default'):
    global _cached_app
    if _cached_app is None:
        _cached_app = create_app(config_name)
    return _cached_app

app = create_or_get_app('default')

if 'migrate' not in app.extensions:
    migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Post=Post,
        TokenBlocklist=TokenBlocklist,
        Role=Role,
        Follow=Follow,
        Comment=Comment,
        Message=Message,
        PostLike=PostLike
    )


@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

# @app.errorhandler(405)
# def method_not_allowed(e):
#     return abort(400, {"msg": 'custom error message to appear in body'})
