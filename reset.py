from Vampiro import create_app
from Vampiro.database.mysql import db

app = create_app()

with app.app_context():
    db.drop_all()  # Drop all tables
    db.create_all()  # Create all tables based on the models