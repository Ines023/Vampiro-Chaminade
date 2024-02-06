# Vampiro/models/NewsletterModel.py
from Vampiro.database.mysql import db

class Cronicas(db.Model):

    date = db.Column(db.Date, nullable=False, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(2000), nullable=False)