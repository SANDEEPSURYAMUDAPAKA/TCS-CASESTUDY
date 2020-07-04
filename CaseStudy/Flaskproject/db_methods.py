from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash
from Flaskproject import db  # db is the SQLAlchemy object created in app.py
from Flaskproject.models import UserStore, Patients, Medicines,MedicineRecord,Diagnostics,Tests


# Authenticate User
def authenticate_user(user, password):
    user = UserStore.query.get(user)
    if user:
        return check_password_hash(user.password, password)  # Returns True if password entered is correct
    return False


# Add Patient
def add_patient(ssn, name, age, doa, room, address, city, state):
    try:
        patient = Patients(ssn=ssn, name=name, age=age, doa=doa, room=room, address=address, city=city, state=state)
        db.session.add(patient)
        db.session.commit()
        return True  # When the new patient added successfully
    except SQLAlchemyError as error:
        return error


# Get Patient
def get_patient(pid):
    return Patients.query.get(pid)


# Update Patient
def update_patient(pid, name, age, doa, room, address, city, state):
    patient = Patients.query.get(pid)
    if patient:
        try:
            patient.name = name
            patient.age = age
            patient.doa = doa
            patient.room = room
            patient.address = address
            patient.city = city
            patient.state = state
            db.session.commit()
            return True  # When the patient's details are updated successfully
        except SQLAlchemyError as error:
            return error
    return False
def checkavailblity(name):
    c = db.session.query(Medicines.name).all()
    Mlist = [item for t in c for item in t]
    flag = name.lower() in (string.lower() for string in Mlist)
    return flag

def getmname(name):
    return Medicines.query.filter(func.lower(Medicines.name) == func.lower(name)).first().mid

Missued = []
def getmissued(mid,mname,quantity):
    rate = Medicines.query.get(mid).rate
    list1 = []
    list1.append(mname)
    list1.append(quantity)
    list1.append(rate)
    Missued.append(list1)

def updaterecord(obj):
    Missued.clear()
    if obj:
        try:
            for o in obj:
                print("commit")
                db.session.add(o)
                db.session.commit()
        except SQLAlchemyError as error:
            print(error)


def perform_billing(pid, dod):
    patient = Patients.query.get(pid)
    if patient:
        patient_details = [pid, patient.name, patient.age, patient.address, patient.doa, dod, patient.room]
        # Room's bill
        no_of_days = (dod - patient.doa).days
        room_bill = 0
        if patient.room == "General Ward":
            room_bill = no_of_days * 2000
        elif patient.room == "Semi Sharing":
            room_bill = no_of_days * 4000
        else:
            room_bill = no_of_days * 8000
        # Medicines' bill
        medicine_records = MedicineRecord.query.filter_by(pid=pid).all()
        pharmacy_bill_rows = []
        pharmacy_bill = 0
        for record in medicine_records:
            m_id = record.mid
            m_issued = record.issued
            m_name = Medicines.query.get(m_id).name
            m_rate = Medicines.query.get(m_id).rate
            m_amount = m_rate * m_issued
            pharmacy_bill += m_amount
            row = [m_name, m_issued, m_rate, m_amount]
            pharmacy_bill_rows.append(row)
        # Diagnostics' bill
        diagnostics_records = Diagnostics.query.filter_by(pid=pid).all()
        diagnostics_bill_rows = []
        diagnostics_bill = 0
        for record in diagnostics_records:
            d_id = record.tid
            d_name = Tests.query.get(d_id).name
            d_charge = Tests.query.get(d_id).charge
            diagnostics_bill += d_charge
            row = [d_name, d_charge]
            diagnostics_bill_rows.append(row)
        total_bill = room_bill + pharmacy_bill + diagnostics_bill
        all_data = [patient_details, no_of_days, room_bill, pharmacy_bill_rows, pharmacy_bill, diagnostics_bill_rows, diagnostics_bill, total_bill]
        return all_data
    else:
        return False


def checkavailblity(name):
    c = db.session.query(Medicines.name).all()
    Mlist = [item for t in c for item in t]
    flag = name.lower() in (string.lower() for string in Mlist)
    return flag

def getmname(name):
    return Medicines.query.filter(func.lower(Medicines.name) == func.lower(name)).first().mid

Missued = []
def getmissued(mid,mname,quantity):
    rate = Medicines.query.get(mid).rate
    list1 = []
    list1.append(mname)
    list1.append(quantity)
    list1.append(rate)
    Missued.append(list1)

def updaterecord(obj):
    Missued.clear()
    if obj:
        try:
            for o in obj:
                db.session.merge(o)
                db.session.commit()
        except SQLAlchemyError as error:
            print(error)


def updatemstore(mid,quant):
    M = Medicines.query.get(mid)
    M.quantity = M.quantity - quant
    db.session.commit()

def getQuantity(pid,mid):
    try:
        q = MedicineRecord.query.filter(MedicineRecord.pid == pid, MedicineRecord.mid == mid).one().issued
    except SQLAlchemyError as error:
        print(error)
        return False
    return q

# View Diagnostic Record
def view_diagnostics(pid):
    patient = Patients.query.get(pid)
    if patient:
        patient_detail = [patient.pid, patient.name, patient.age, patient.doa, patient.room, patient.address,
                          patient.state, patient.city]
        diagnostics_conducted = [r[0] for r in db.session.query(Diagnostics.tid).filter(Diagnostics.pid == pid).all()]
        diagnostics_records = []
        for d in diagnostics_conducted:
            diagnostics_records.append(db.session.query(Tests.name, Tests.charge).filter(Tests.tid == d).all())
        diagnostics_records = [r for r, in diagnostics_records]
        result = [patient_detail, diagnostics_records]
        return result
    else:
        return False


# Tests Select Fields
def test_choices(pid):
    all_tests = [r for r, in db.session.query(Tests.name).all()]  # Contains all tests performed in the hospital
    performed_tests = [r for r, in db.session.query(Tests.name).join(Diagnostics).filter(Diagnostics.pid == pid).all()]
    avl_tests = list(filter(lambda x: x not in performed_tests, all_tests))
    return list(tuple(zip(avl_tests, avl_tests)))


# Returns new_rows in addDiagnostics method in route.py
def add_diagnostics_row(tests):
    all_tests = []
    for test in tests:
        all_tests.append(db.session.query(Tests.name, Tests.charge).filter(Tests.name == test).all())
    all_tests = [r for r, in all_tests]
    return all_tests


# Updates the new diagnostics for a patient in Diagnostics
def update_diagnostics(pid, tests):
    try:
        for test in tests:
            to = Tests.query.filter_by(name=test).first()
            db.session.add(Diagnostics(pid=pid, tid=to.tid))
            db.session.commit()
        return True
    except SQLAlchemyError as error:
        return False
def delete_patient(pid):
    try:
        patient = Patients.query.get(pid)
        db.session.delete(patient)
        db.session.commit()
        all_diagnostics = Diagnostics.query.filter_by(pid=pid).all()
        all_medicines_record = MedicineRecord.query.filter_by(pid=pid).all()
        for d in all_diagnostics:
            db.session.delete(d)
            db.session.commit()
        for m in all_medicines_record:
            db.session.delete(m)
            db.session.commit()
        return True
    except SQLAlchemyError as error:
        return True