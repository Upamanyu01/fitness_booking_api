from app.models import FitnessClass
from app import db
from datetime import datetime, timedelta
from app.utils import to_utc

def seed_data():
    if not FitnessClass.query.first():
        classes = [
            FitnessClass(name="Yoga", instructor="Anita", datetime=to_utc(datetime.now() + timedelta(days=1, hours=9)), available_slots=5),
            FitnessClass(name="Zumba", instructor="Rahul", datetime=to_utc(datetime.now() + timedelta(days=2, hours=11)), available_slots=10),
            FitnessClass(name="HIIT", instructor="Vikram", datetime=to_utc(datetime.now() + timedelta(days=3, hours=8)), available_slots=8),
        ]
        db.session.bulk_save_objects(classes)
        db.session.commit()
