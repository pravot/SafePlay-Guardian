from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exclusions.db'
    app.secret_key = os.getenv('FLASK_SECRET_KEY')

    # Initialize the app with the db instance
    db.init_app(app)

    with app.app_context():
        # Import and register the blueprint
        from .routes import bp as main_bp
        app.register_blueprint(main_bp)

        # Create the database tables
        db.create_all()

    return app
