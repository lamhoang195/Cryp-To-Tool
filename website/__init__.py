from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .scripts.rsa import rsa
    from .scripts.elgamal import elgamal
    from .scripts.elliptic import elliptic
    from .scripts.elliptic_sig import elliptic_signature

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(rsa, url_prefix='/rsa')
    app.register_blueprint(elgamal, url_prefix='/elgamal')
    app.register_blueprint(elliptic, url_prefix='/elliptic')
    app.register_blueprint(elliptic_signature, url_prefix='/elliptic_signature')
    from .models import User

    create_database(app)
  
    login_manager = LoginManager()
    login_manager.login_view = 'views.home'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created database!')