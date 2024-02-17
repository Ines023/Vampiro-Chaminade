import os
from datetime import datetime
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager, current_user

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
    from Vampiro.models.UserModel import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    login_manager.login_view = 'public.login'

    # BLUEPRINTS _______________________________________________________________

    from .views.AdminViews import admin
    from .views.PublicViews import public
    from .views.ProfileViews import profile
    from .views.AutomationsViews import automation
    
    app.register_blueprint(public, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(automation, url_prefix='/automation')

    from Vampiro.services.settings import get_round_status, get_game_status
    @app.context_processor
    def inject_game_status_and_user_role():
        game_status = get_game_status()
        round_status = get_round_status()
        user_role = current_user.role.name if current_user.is_authenticated else 'guest'
        return dict(game_status=game_status.name, user_role=user_role, round_status=round_status)


    # DATABASE _________________________________________________________________
    db.init_app(app)

    from Vampiro.models.UserModel import User, Role, Player, Hunt, Dispute
    from Vampiro.models.NewsletterModel import Cronicas
    from Vampiro.models.SettingsModel import Settings

    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

        # Initial setting creation
        if Settings.query.count() == 0:
            settings = Settings( mode='VAMPIRO', game_status='NOT_STARTED', round_status='PROCESSED', extension_status='NOT_EXTENDED', timer_switch=False, holidays=False)
            db.session.add(settings)

        # Check if roles already exist
        if Role.query.count() == 0:
            roles = [('admin','Game Organizer'), ('player','User participating as a player'), ('visitor','Registered user not involved in any games')]  # Add your roles here
            for role in roles:
                db.session.add(Role(name=role[0], description=role[1]))

        # Check if admin user already exists
        if User.query.filter_by(name='Dracula').first() is None:
            admin_role = Role.query.filter_by(name='admin').first()
            id=900

            admin = User(id=id, name='Dracula', password=os.getenv('ADMIN_PASSWORD'), email=os.getenv('ADMIN_EMAIL'), active=True, confirmed_at=datetime.now().date(), role=admin_role)
            db.session.add(admin)

        db.session.commit()

    return app