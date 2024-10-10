from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate  # Import Migrate
from flask_jwt_extended import JWTManager  # Import JWTManager

# Initialize the database and migration objects
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()  # Initialize JWTManager
DB_NAME = "whiskey"

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = '4796f7276f9242b4bb7899907b8c62e7'
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'postgresql://postgres.ffeahodvdatbkywcmcvu:164748Cajh!@aws-0-us-east-1.pooler.supabase.com:6543/postgres'
    )
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change to your actual secret key

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Migrate with app and db
    jwt.init_app(app)  # Initialize JWTManager with app

    # Import and register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models to ensure they are registered with SQLAlchemy
    from .models import User, Note

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Set up the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


