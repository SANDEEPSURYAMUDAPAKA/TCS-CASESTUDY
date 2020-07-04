# This file contains all table models
from Flaskproject import db  # db is the SQLAlchemy object created in app.py
from flask_login import UserMixin
from datetime import datetime, date


# -----------------------------------------------------------------------------------------
# ----------------------------------- TABLE MODELS ----------------------------------------
# Users table model
class UserStore(UserMixin, db.Model):
    user = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.TIMESTAMP(), nullable=False, default=datetime.now())

    # This method specifies what will be printed if we print the User object
    def __repr__(self):
        return f"UserStore('{self.user}', '{self.timestamp}')"

    def get_id(self):
           return (self.user)
# Patient table model
class Patients(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.String(9), unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    doa = db.Column(db.Date, nullable=False, default=date.today())
    room = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='Active')

    # This method specifies what will be printed if we print the User object
    def __repr__(self):
        return f"Patients('{self.pid}', '{self.ssn}', '{self.name}', '{self.age}', '{self.doa}', '{self.room}', '{self.address}', '{self.city}', '{self.state}', '{self.status}')"


# Medicine master table model
class Medicines(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Float, nullable=False)

    # This method specifies what will be printed if we print the Medicines object
    def __repr__(self):
        return f"Medicines('{self.mid}', '{self.name}', '{self.quantity}' '{self.rate}')"


# Diagnostics master table model
class Tests(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    charge = db.Column(db.Float, nullable=False)

    # This method specifies what will be printed if we print the Tests object
    def __repr__(self):
        return f"Tests('{self.tid}', '{self.name}', '{self.charge}')"


# Patient medicine record table model
class MedicineRecord(db.Model):
    pid = db.Column(db.Integer, db.ForeignKey('patients.pid'), primary_key=True, nullable=False)
    mid = db.Column(db.Integer, db.ForeignKey('medicines.mid'), primary_key=True, nullable=False)
    issued = db.Column(db.Integer, nullable=False)

    # This method specifies what will be printed if we print the Medicine Record object
    def __repr__(self):
        return f"MedicineRecord('{self.pid}', '{self.mid}', '{self.issued}')"


# Patient diagnostics record table model
class Diagnostics(db.Model):
    pid = db.Column(db.Integer, db.ForeignKey('patients.pid'), primary_key=True, nullable=False)
    tid = db.Column(db.Integer, db.ForeignKey('tests.tid'), primary_key=True, nullable=False)

    # This method specifies what will be printed if we print the Diagnostics object
    def __repr__(self):
        return f"Diagnostics('{self.pid}', '{self.tid}')"
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

