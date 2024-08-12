from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from . import db
from .models import Exclusion
from sqlalchemy.exc import IntegrityError

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/add_exclusion', methods=['GET', 'POST'])
def add_exclusion_page():
    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "date_of_birth": request.form['date_of_birth'],
            "gender": request.form['gender'],
            "street": request.form['street'],
            "city": request.form['city'],
            "state": request.form['state'],
            "zip": request.form['zip'],
            "reason": request.form['reason'],
            "start_date": request.form['start_date'],
            "end_date": request.form['end_date'],
            "exclusion_authority": request.form['exclusion_authority'],
            "notes": request.form['notes'],
            "id_type": request.form['id_type'],
            "id_number": request.form['id_number']
        }
        try:
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

@bp.route('/exclusions/<id_number>', methods=['GET'])
def get_exclusion_api(id_number):
    exclusion = Exclusion.query.filter_by(id_number=id_number).first()
    if exclusion:
        exclusion_data = {
            'id': exclusion.id,
            'name': exclusion.name,
            'date_of_birth': exclusion.date_of_birth,
            'gender': exclusion.gender,
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
            'id_number': exclusion.id_number
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
            'id': exclusion.id,
            'name': exclusion.name,
            'date_of_birth': exclusion.date_of_birth,
            'gender': exclusion.gender,
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
            'id_number': exclusion.id_number
        })
    return jsonify(exclusion_list)
