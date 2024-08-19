from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from . import db
from .models import Exclusion
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import os

bp = Blueprint('main', __name__)

UPLOAD_FOLDER = 'static/mugshots/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure the directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/add_exclusion', methods=['GET', 'POST'])
def add_exclusion_page():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form['first_name']
        middle_name = request.form.get('middle_name', '')
        last_name = request.form['last_name']
        aliases = request.form.get('aliases', '')
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        race = request.form['race']
        hair_color = request.form['hair_color']
        height = request.form['height']
        eye_color = request.form['eye_color']
        weight = request.form['weight']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip']
        reason = request.form['reason']
        start_date = request.form['start_date']
        exclusion_authority = request.form['exclusion_authority']
        notes = request.form.get('notes')
        id_type = request.form['id_type']
        id_number = request.form['id_number']

        # Calculate end date based on reason and start date
        start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
        exclusion_duration = {
            'Cheating': 2,
            'Fraud': 3,
            'Violence': 5,
            'Theft': 4,
        }.get(reason, 1)
        end_date_dt = start_date_dt.replace(year=start_date_dt.year + exclusion_duration)

        # Handle mugshot file upload
        mugshot_data = None
        mugshot = request.files['mugshot']
        if mugshot and allowed_file(mugshot.filename):
            mugshot_data = mugshot.read()

        # Prepare data for the new Exclusion record
        data = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "aliases": aliases,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "race": race,
            "hair_color": hair_color,
            "height": height,
            "eye_color": eye_color,
            "weight": weight,
            "street": street,
            "city": city,
            "state": state,
            "zip": zip_code,
            "reason": reason,
            "start_date": start_date_dt,
            "end_date": end_date_dt,
            "exclusion_authority": exclusion_authority,
            "notes": notes,
            "id_type": id_type,
            "id_number": id_number,
            "mugshot_data": mugshot_data
        }

        try:
            # Attempt to add the new exclusion to the database
            new_exclusion = Exclusion(**data)
            db.session.add(new_exclusion)
            db.session.commit()
            flash('Exclusion added successfully!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Exclusion with this ID number already exists!', 'danger')

        return redirect(url_for('main.add_exclusion_page'))

    return render_template('add_exclusion.html')

@bp.route('/view_exclusions', methods=['GET'])
def view_exclusions_page():
    exclusions = Exclusion.query.all()
    return render_template('view_exclusions.html', exclusions=exclusions)

@bp.route('/exclusions/<registration_number>', methods=['GET'])
def get_exclusion_api(registration_number):
    exclusion = Exclusion.query.filter_by(registration_number=registration_number).first()
    if exclusion:
        exclusion_data = {
            'registration_number': exclusion.registration_number,
            'first_name': exclusion.first_name,
            'middle_name': exclusion.middle_name,
            'last_name': exclusion.last_name,
            'aliases': exclusion.aliases,
            'date_of_birth': exclusion.date_of_birth,
            'gender': exclusion.gender,
            'race': exclusion.race,
            'hair_color': exclusion.hair_color,
            'height': exclusion.height,
            'eye_color': exclusion.eye_color,
            'weight': exclusion.weight,
            'street': exclusion.street,
            'city': exclusion.city,
            'state': exclusion.state,
            'zip': exclusion.zip,
            'reason': exclusion.reason,
            'start_date': exclusion.start_date,
            'end_date': exclusion.end_date,
            'exclusion_authority': exclusion.exclusion_authority,
            'notes': exclusion.notes,
            'id_type': exclusion.id_type,
            'id_number': exclusion.id_number,
            'mugshot_data': exclusion.mugshot_data
        }
        return jsonify(exclusion_data)
    else:
        return jsonify({'message': 'Exclusion not found'}), 404

@bp.route('/exclusions', methods=['GET'])
def view_exclusions_api():
    exclusions = Exclusion.query.all()
    exclusion_list = []
    for exclusion in exclusions:
        exclusion_list.append({
            'registration_number': exclusion.registration_number,
            'first_name': exclusion.first_name,
            'middle_name': exclusion.middle_name,
            'last_name': exclusion.last_name,
            'aliases': exclusion.aliases,
            'date_of_birth': exclusion.date_of_birth,
            'gender': exclusion.gender,
            'race': exclusion.race,
            'hair_color': exclusion.hair_color,
            'height': exclusion.height,
            'eye_color': exclusion.eye_color,
            'weight': exclusion.weight,
            'street': exclusion.street,
            'city': exclusion.city,
            'state': exclusion.state,
            'zip': exclusion.zip,
            'reason': exclusion.reason,
            'start_date': exclusion.start_date,
            'end_date': exclusion.end_date,
            'exclusion_authority': exclusion.exclusion_authority,
            'notes': exclusion.notes,
            'id_type': exclusion.id_type,
            'id_number': exclusion.id_number,
            'mugshot_data': exclusion.mugshot_data
        })
    return jsonify(exclusion_list)
