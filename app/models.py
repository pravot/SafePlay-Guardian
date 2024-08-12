from . import db

class Exclusion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    street = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(10), nullable=False)
    end_date = db.Column(db.String(10), nullable=False)
    exclusion_authority = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    id_type = db.Column(db.String(20), nullable=False)
    id_number = db.Column(db.String(20), nullable=False, unique=True)
