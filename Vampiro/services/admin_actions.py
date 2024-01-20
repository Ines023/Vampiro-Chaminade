from Vampiro.database.mysql import db

# CRONICAS _________________________________________________________________

def add_cronica(cronica):
    db.session.add(cronica)
    db.session.commit()



