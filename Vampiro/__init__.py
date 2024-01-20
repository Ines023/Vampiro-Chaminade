import os
from datetime import datetime
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from models.UserModel import User

from .database.mysql import db
from config import Config

login_manager = LoginManager()

def create_app(config_class=Config, test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # CONFIG ___________________________________________________________________
    app.config.from_object(config_class)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # LOGIN MANAGER ____________________________________________________________
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # BLUEPRINTS _______________________________________________________________

    from .views.AdminViews import admin
    from .views.PublicViews import public
    from .views.ProfileViews import profile
    
    app.register_blueprint(public, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(profile, url_prefix='/profile')

    # DATABASE _________________________________________________________________
    db.init_app(app)

    from models.UserModel import User, Role, Player, Hunt, Dispute, roles_users
    from models.NewsletterModel import Cronicas
    from models.SettingsModel import Settings

    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

        # Check if roles already exist
        if Role.query.count() == 0:
            roles = ['admin', 'player', 'visitor']  # Add your roles here
            for role in roles:
                db.session.add(Role(name=role))

        # Check if admin user already exists
        if User.query.filter_by(name='Dracula').first() is None:
            admin_role = Role.query.filter_by(name='admin').first()
            id=999

            admin = User(id=999, name='Dracula', password=os.getenv('ADMIN_PASSWORD'), email=os.getenv('ADMIN_EMAIL'), active=True, confirmed_at=datetime.now().date(), role=admin_role)
            db.session.add(admin)

        db.session.commit()



    return app