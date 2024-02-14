# Vampiro/models/NewsletterModel.py
from Vampiro.database.mysql import db

class Cronicas(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(2000), nullable=False)