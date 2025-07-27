from flask import Blueprint, request, jsonify
from app import db
from app.models import FitnessClass, Booking
from app.utils import  from_utc
import logging

bp = Blueprint('routes', __name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@bp.route('/classes', methods=['GET'])
def get_classes():
    try:
        tz = request.args.get('tz', 'Asia/Kolkata')
        classes = FitnessClass.query.all()
        result = []
        for c in classes:
            result.append({
                'id': c.id,
                'name': c.name,
                'instructor': c.instructor,
                'datetime': from_utc(c.datetime, tz).strftime('%Y-%m-%d %H:%M'),
                'available_slots': c.available_slots
            })
        return jsonify(result), 200
    except Exception as e:
        logger.exception("Error fetching classes")
        return jsonify({'error': 'An error occurred while retrieving classes.'}), 500

@bp.route('/book', methods=['POST'])
def book_class():
    try:
        data = request.get_json()
        required = ['class_id', 'client_name', 'client_email']
        if not all(k in data for k in required):
            return jsonify({'error': 'Missing required fields'}), 400

        fitness_class = FitnessClass.query.get(data['class_id'])
        if not fitness_class:
            return jsonify({'error': 'Class not found'}), 404

        if fitness_class.available_slots <= 0:
            return jsonify({'error': 'No slots available'}), 409

        booking = Booking(
            class_id=fitness_class.id,
            client_name=data['client_name'],
            client_email=data['client_email']
        )
        db.session.add(booking)
        fitness_class.available_slots -= 1
        db.session.commit()

        return jsonify({'message': 'Booking successful'}), 201

    except Exception as e:
        logger.exception("Booking error")
        return jsonify({'error': 'An error occurred'}), 500

@bp.route('/bookings', methods=['GET'])
def get_bookings():
    try:
        email = request.args.get('email')
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        bookings = Booking.query.filter_by(client_email=email).all()
        result = []
        for b in bookings:
            cls = FitnessClass.query.get(b.class_id)
            result.append({
                'booking_id': b.id,
                'class_name': cls.name,
                'datetime': from_utc(cls.datetime).strftime('%Y-%m-%d %H:%M'),
                'instructor': cls.instructor
            })
        return jsonify(result), 200
    except Exception as e:
        logger.exception("Error fetching bookings")
        return jsonify({'error': 'An error occurred while retrieving bookings.'}), 500
