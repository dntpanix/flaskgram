
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from app.extinsions import db, migrate, login_manager, mail, dropzone, csrf, search
from app.commands import create_tables, delete_tables, del_user
from app.user import user
from app.main import main
from app.post import post

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
    login_manager.init_app(app)
    mail.init_app(app)
    dropzone.init_app(app)
    csrf.init_app(app)
    search.init_app(app)

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

    # @app.route('/')
    # def index():
    #     return render_template('index.html')
    
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(post, url_prefix='/post')
    app.register_blueprint(main)

    app.cli.add_command(create_tables)
    app.cli.add_command(delete_tables)
    app.cli.add_command(del_user)


    return app
