from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


def get_user_by_name(username):
    user = User.query.filter_by(name=username).first()
    if user:
        user_data = {
            'id': user.id,
            'name': user.name,
            'password': user.password
        }
        return user_data
    else:
        return None


def add_user(username, password):
    new_user = User(name=username, password=password)

    db.session.add(new_user)
    db.session.commit()
