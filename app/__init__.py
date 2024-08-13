from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import base64

# Initialize SQLAlchemy instance
db = SQLAlchemy()


def create_app():
    load_dotenv()

    app = Flask(__name__)

    # MariaDB connection URI
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

    app.secret_key = os.getenv('FLASK_SECRET_KEY')

    # Define the base64 encoding filter
    def b64encode_filter(data):
        if data is None:
            return ''
        return base64.b64encode(data).decode('utf-8')

    # Register the filter with the Jinja2 environment
    app.jinja_env.filters['b64encode'] = b64encode_filter

    # Initialize the app with the db instance
    db.init_app(app)

    with app.app_context():
        # Import and register the blueprint
        from .routes import bp as main_bp
        app.register_blueprint(main_bp)

        # Create the database tables
        db.create_all()

    return app
