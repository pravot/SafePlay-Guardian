from . import db
from datetime import datetime


class Exclusion(db.Model):
    __tablename__ = 'exclusion'

    # The registration number serves as the primary key
    registration_number = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Personal details
    first_name = db.Column(db.String(80), nullable=False)
    middle_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=False)
    aliases = db.Column(db.String(255), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    race = db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    height = db.Column(db.String(10), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    # Address details
    street = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    zip = db.Column(db.String(10), nullable=False)

    # Offense details
    reason = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    exclusion_authority = db.Column(db.String(100), nullable=False)

    # Additional details
    notes = db.Column(db.Text, nullable=True)
    id_type = db.Column(db.String(20), nullable=False)
    id_number = db.Column(db.String(20), nullable=False, unique=True)

    # Mugshot stored as binary data
    mugshot_data = db.Column(db.LargeBinary(length=(2 ** 32) - 1), nullable=True)  # LONGBLOB to store large binary data

    @property
    def age(self):
        """Calculate age from date_of_birth"""
        return datetime.now().year - self.date_of_birth.year
