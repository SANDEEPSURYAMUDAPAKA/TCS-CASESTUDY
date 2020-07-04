from datetime import date

from flask import render_template, redirect, url_for, flash, session, request
from flask_login import LoginManager, login_user, login_required

from Flaskproject import app
from Flaskproject.Forms import PatientForm, IssueMedicines, SearchForPatient, Diagnostic, Billing, LoginForm, \
    DeletePatient, EditPatient, getid, GetQuantity, updatemrecord, AddDiagnostics
from Flaskproject.db_methods import *
from Flaskproject.models import UserStore, Patients, Medicines, MedicineRecord

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

objlist=[]
tests = []
#----------------------------------------------------------Login_manager----------------------------------------------------------------#
@login_manager.user_loader
def load_user(user) :
    return UserStore.query.get(user)

#----------------------------------------------------------Login User-------------------------------------------------------------------#
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login() :
    form = LoginForm()
    if form.validate_on_submit() :
        if authenticate_user(form.user.data,form.password.data):
            session["user"] = form.user.data
            login_user(UserStore.query.get(form.user.data))
            flash("Login succesfully", "alert alert-success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or Password","alert alert-danger")
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('login.html', form=form)


#-----------------------------------------------------------Home Page----------------------------------------------------------------------#
@app.route('/home')
@login_required
def home() :
    if "user" in session :
        user = session["user"]
        return render_template('home.html', home=True)
    else :
        return redirect(url_for('login'))


# ------------------------------------------------------ExecutiveDesk-----------------------------------------------------------------------#

#--------------------------------------------------------CreatePatient----------------------------------------------------------------------#
@app.route('/CreatePatient',methods=['GET','POST'])
@login_required
def CreatePatient() :
    if "user" in session :
        user = session["user"]
        form = PatientForm()
        if user == "Executive" :
            if form.validate_on_submit() and request.method == "POST" :
                p=add_patient(int(form.PatientSSNId.data),form.patientNAME.data,int(form.patientAGE.data),form.patientDOA.data,form.TOB.data,form.ADDRESS.data,form.CITY.data,form.STATE.data)
                flash("Patient creation initiated successfully", "alert alert-success")
                print(p)
            return render_template('CreatePatient.html', form=form)
        else :
            flash(" Only Executive can access this feature", "danger")
            return redirect(url_for("home"))
    else :
        return redirect(url_for("login"))

#-------------------------------------------------------View All Patients---------------------------------------------------------------------------#
@app.route('/ViewAllPatients',methods=['GET','POST'])
@login_required
def viewAllPatients() :
    if "user" in session :
        user = session["user"]
        if user == "Executive" :
            ap = Patients.query.filter_by(status="Active").all()
            for p in ap:
                print(p.ssn)

            return render_template('ViewAllPatients.html',ap=ap)
        else :
            flash(" Only Executive can access this feature", "danger")
            return redirect(url_for("home"))
    else :
        return redirect(url_for("login"))

#------------------------------------------------------Search For Patients--------------------------------------------------------------------------#
@app.route('/SearchForPatients',methods=['GET', 'POST'])
@login_required
def searchForPatients() :
    if "user" in session :
        user = session["user"]
        if user == "Executive" :
            form = SearchForPatient()
            if form.validate_on_submit() and request.method == "POST" :
                data = get_patient(int(form.PatientId.data))
                if (data!=None):
                    flash("Patient found", "alert alert-success")
                    return render_template('SearchForPatients.html', form=form, data=data)
                else:
                    flash("Incorrect Id", "alert alert-danger")
                    return render_template('SearchForPatients.html', form=form)
            else:
                return render_template('SearchForPatients.html', form=form)
        else :
            flash(" Only Executive can access this feature", "danger")
            return redirect(url_for("home"))
    else :
        return redirect(url_for("login"))
#----------------------------------------------------------Delete Patient---------------------------------------------------------------------#
@app.route('/DeletePatient',methods=['GET','POST'])
@login_required
def deletepatient() :
    if "user" in session :
        user = session["user"]
        if user == "Executive" :
            form = DeletePatient()
            if form.validate_on_submit() and request.method == "POST" :
                data = get_patient(int(form.PatientId.data))
                if (data != None):
                    return render_template('DeletePatient.html', form=form, data=data,
                                           flash=flash("Patient found", "alert alert-success"))
                else:
                    return render_template('DeletePatient.html', form=form,
                                           flash=flash("Incorrect Id", "alert alert-danger"))
            else:
                return render_template('DeletePatient.html', form=form)
        else :
            flash(" Only Executive can access this feature", "danger")
            return redirect(url_for("home"))
    else:
            return redirect(url_for("login"))
@app.route('/DeletePatient/<int:pid>')
def delete(pid):
    if delete_patient(pid):
        flash("Deletion Successful", "alert alert-success")
        return redirect('/DeletePatient')
    return redirect('/DeletePatient')
#---------------------------------------Edit Patient-----------------------------------------------------------------------#

@app.route('/EditPatient', methods=['GET', 'POST'])
@login_required
def editPatient():
    if "user" in session:
        user = session["user"]
        form = getid()
        if user == "Executive":
            form= getid()
            if form.validate_on_submit() and request.method == "POST":
                data = get_patient(int(form.PatientId.data))
                if (data != None):
                    return render_template('EditPatient.html', form=form, data=data, flash=flash("Patient found", "alert alert-success"))
                else:
                    return render_template('EditPatient.html', form=form, data=data, flash=flash("Incorrect Id", "alert alert-danger"))
            else:
                return render_template('EditPatient.html', form=form)
        else :
            flash(" Only Executive can access this feature", "danger")
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))



@app.route('/EditPatient2/<int:pid>', methods=['GET', 'POST'])
@login_required
def editPatient2(pid):
    if "user" in session:
        data = None
        user = session["user"]       
        if user == "Executive":
            form = EditPatient()
            if form.validate_on_submit() and request.method == "POST":
                update_patient(pid,form.patientNAME.data, form.patientAGE.data, form.patientDOA.data, form.TOB.data, form.ADDRESS.data, form.CITY.data, form.STATE.data )
                db.session.commit()
                return redirect('/ViewAllPatients')
            return render_template('EditPatient2.html', form=form, patient=Patients.query.get(int(pid)))
        else :
            flash(" Only Executive can access this feature", "danger")
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

#------------------------------------Billing ---------------------------------------------------------------------------------------------#
@app.route('/Billing', methods=['GET','POST'])
@login_required
def billing():
    if "user" in session:
        user = session["user"]
        if user == "Executive":
            form = Billing()
            if form.validate_on_submit():
                pid = int(form.PatientId.data)
                bill = perform_billing(pid, date.today())
                if bill:
                    # Patients.query.get(pid).status = 'Discharged'
                    # db.session.commit()
                    return render_template('Billing.html', form=form, bill=bill, pid=pid)
                else:
                    flash("Invalid patient id", "danger")
                    return render_template('Billing.html', form=form, pid=pid)
            else:
                return render_template('Billing.html', form=form)
        else:
            flash(" Only Executive can access this feature", "danger")
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route('/Billing/<int:pid>', methods=['GET', 'POST'])
@login_required
def confirm_billing(pid):
    if "user" in session:
        user = session["user"]
        if user == "Executive":
            form = Billing()
            if Patients.query.get(pid):
                if Patients.query.get(pid).status == 'Discharged':
                    flash(f"Billing of Patient with id { pid } already done", "danger")
                    return redirect(url_for('billing'))
            Patients.query.get(pid).status = 'Discharged'
            db.session.commit()
            flash("Patient status changed to 'Discharged'", "success")
            return redirect(url_for('billing'))
        else:
            flash(" Only Executive can access this feature", "danger")
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

# ----------------------------------------Pharmacy------------------------------------------------------------------------------------#

#----------------------------------------------View Patient Pharma Details------------------------------------------------------------#

@app.route('/PharmaViewPatientsDetail',methods=['GET','POST'])
@login_required
def pharmaViewPatientsDetail() :
    if "user" in session :
        user = session["user"]
        if user == "Pharmacist" :
            form = SearchForPatient()
            if form.validate_on_submit() and request.method == "POST":
                data = Patients.query.get(int(form.PatientId.data))
                Mdetails =db.session.query(Medicines,MedicineRecord).join(MedicineRecord).filter(MedicineRecord.pid==(int(form.PatientId.data))).all()
                if (data != None):
                    session["pid"] = int(form.PatientId.data)
                    return render_template('PharmaViewPatientsDetail.html', form=form, data=data,Mdetails=Mdetails,flash=flash("Patient found", "alert alert-success"))
                else:
                    return render_template('PharmaViewPatientsDetail.html', form=form,flash=flash("Incorrect Id", "alert alert-danger"))
            else:
                return render_template('PharmaViewPatientsDetail.html', form=form)
        else :
            flash(" Only Pharmacist can access this feature", "danger")
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

## I have add 4 methodes to db_methods.py checkavailblity,getname,updaterecord,getmissued,getquantity,updatemstore also need to add func from sqlalchemy package
# added 2 new forms getquantity and updatemrecord
#declared one global veriable in routes.py objlist
# ----------------------------------------------Issue Medicine----------------------------------------------------------------------
@app.route('/IssueMedicines',methods=['GET','POST'])
@login_required
def issueMedicines() :
    if "user" in session :
        user = session["user"]
        if user == "Pharmacist" :
            form = IssueMedicines()
            form2 = GetQuantity()
            form3 = updatemrecord()
            # route for checkavailablity and adding name and id of medicine to session
            if form.validate_on_submit() and request.method == "POST":
                session["mname"] = form.MedicineName.data
                flag=checkavailblity(form.MedicineName.data)
                if flag==True:
                    session["mid"] = getmname(form.MedicineName.data)
                    session["QuantityAvail"] = Medicines.query.get(session["mid"]).quantity

                else:
                    session["QuantityAvail"]=0
                return render_template('IssueMedicines.html',form=form,flag=flag,check=True,form2=form2,QuantityAvail=session["QuantityAvail"])

            # route for adding and displaying newly added medicine
            elif form2.validate_on_submit() and request.method == "POST":
                if int(form2.Quantity.data) <= session["QuantityAvail"]:
                    pid = session["pid"]
                    mid = session["mid"]
                    issue = int(form2.Quantity.data)
                    session["issue"] = issue
                    q = getQuantity(pid,mid)
                    if q:
                        m = MedicineRecord(pid=pid,mid=mid,issued=issue+q)
                    else:
                        m = MedicineRecord(pid=pid,mid=mid,issued=issue)
                    objlist.append(m)
                    getmissued(mid,session["mname"],issue)
                    return render_template('IssueMedicines.html',form=form,flag=True,check=False,form2=form2,Missued=Missued,form3=form3)
                else:
                    return render_template('IssueMedicines.html', form=form, flag=True, check=True, form2=form2,
                                           QuantityAvail=session["QuantityAvail"],flash=flash("Enter Proper Quantity","alert alert-danger"))
            # route to commit to db i.e. to update MedicineRecord and initailize every variable as it is
            elif form3.validate_on_submit() and request.method == "POST":
                updatemstore(session["mid"],session["issue"])
                session.pop("pid", None)
                session.pop("mid", None)
                session.pop("mname", None)
                session.pop("issue", None)
                session.pop("QuantityAvail",None)
                updaterecord(objlist)
                objlist.clear()
                flash(" Medicines issued successfully", "success")
                return redirect(url_for("pharmaViewPatientsDetail"))
            else:
                return render_template('IssueMedicines.html',form=form,check=False)
        else :
            flash(" Only Pharmacist can access this feature", "danger")
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))
#-----------------------------------------------------------Add Diagnostics------------------------------------------------------------------------------------#
@app.route('/Diagnostic', methods=['GET', 'POST'])
@login_required
def diagnostics():
    if "user" in session :
        user = session["user"]
        if user == "Diagnostics":
            form = Diagnostic()
            if form.validate_on_submit():
                pid = int(form.PatientId.data)
                result = view_diagnostics(pid)
                if result:
                    return render_template('Diagnostics.html', form=form, result=result, pid=pid)
                else:
                    flash("Invalid patient id", "danger")
                    return render_template('Diagnostics.html', form=form, pid=pid)
            else:
                return render_template('Diagnostics.html', form=form)
        else :
            flash(" Only Diagnostics can access this feature", "danger")
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route('/AddDiagnostics/<int:pid>', methods=['GET','POST'])
@login_required
def addDiagnostics(pid):
    if "user" in session:
        user = session["user"]
        if user == "Diagnostics":
            form = AddDiagnostics()
            form.diagnostictest.choices = test_choices(pid)
            if form.validate_on_submit():
                tests.append(form.diagnostictest.data)
                form.diagnostictest.choices = test_choices(pid)
                new_rows = add_diagnostics_row(tests)
                if new_rows:
                    return render_template('AddDiagnostics.html', form=form, pid=pid, new_rows=new_rows)
            return render_template('AddDiagnostics.html', form=form, pid=pid)
        else :
            flash(" Only Diagnostics can access this feature", "danger")
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route('/UpdateDiagnostics/<int:pid>', methods=['GET', 'POST'])
@login_required
def updateDiagnostics(pid):
    if "user" in session:
        user = session["user"]
        if user == "Diagnostics":
            if update_diagnostics(pid, tests):
                tests.clear()
                flash(f"New tests records for {pid} updated successfully", "success")
                return redirect(url_for('diagnostics'))
            else:
                flash(f"Some error occurred while updating diagnostics record of {pid}", "danger")
                return redirect(url_for('addDiagnostics', pid=pid))
        else :
            flash(" Only Diagnostics can access this feature", "danger")
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))
#------------------------------------------------------------------Logging Out User------------------------------------------------------------------------------#
@app.route("/logout")
@login_required
def logout() :
    session.pop('user', None)
    return redirect(url_for("login"))
