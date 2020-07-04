from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp


class LoginForm(FlaskForm):
    user = StringField('username', validators=[InputRequired(),Regexp(regex="^[a-zA-Z0-9]+[a-zA-Z0-9]+.{6,32}$"), Length(min=8, max=32)])
    password = PasswordField('password', validators=[InputRequired(),Regexp(regex="^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@#$%^&+=]).{10,32}$"), Length(min=10, max=32)])
#--------------------------------------------------------------Executive---------------------------------------------------------------#
class PatientForm(FlaskForm):
    PatientSSNId = StringField('Patient SSN ID*', validators=[InputRequired(),Length(max=9,min=9,message="SSN ID must be of 9 digits numeric"),Regexp(regex="[0-9]*$",message="Must be numeric")])
    patientNAME =StringField('Patient Name*', validators=[InputRequired(),Regexp(regex="[A-Za-z ]*$",message="Only Alphabets Required")])
    patientAGE = StringField('Patient Age*', validators=[InputRequired(),Length(min=1,max=3,message="Age should be max 3 Digit allowed"),Regexp(regex="[0-9]*$",message="should be numeric value")])
    patientDOA = DateField('Date Of Admission' , format='%Y-%m-%d')
    TOB = SelectField('Type of bed*', choices=[("General Ward","General Ward"), ("Semi Sharing","Semi Sharing"), ("Single Room","Single Room")])
    ADDRESS = StringField('Address*', validators=[InputRequired(),Regexp(regex="[A-Za-z0-9 ,-]*$",message="No special charecter other than space,comma,dash")])
    STATE = StringField('State*', validators=[InputRequired()])
    CITY = StringField('City*', validators=[InputRequired()])

class EditPatient(FlaskForm):
    patientNAME =StringField('Patient Name*', validators=[InputRequired(),Regexp(regex="[A-Za-z ]*$",message="Only Alphabets required")])
    patientAGE = StringField('Patient Age*', validators=[InputRequired(),Length(min=1,max=3,message="Age should be max 3 digit"),Regexp(regex="[0-9]*$",message="should be numeric value")])
    TOB = SelectField('Type of bed*', choices=[("General Ward","General Ward"), ("Semi Sharing","Semi Sharing"), ("Single Room","Single Room")])
    patientDOA = DateField('Date Of Admission' , format='%Y-%m-%d')
    ADDRESS = StringField('Address*', validators=[InputRequired(),Regexp(regex="[A-Za-z0-9 ,-]*$",message="No special charecter other than space,comma,dash")])
    STATE = StringField('State*', validators=[InputRequired(),Regexp(regex="[A-Za-z0-9 ,-]*$",message="only alphanumeric")])
    CITY = StringField('City*', validators=[InputRequired(),Regexp(regex="[A-Za-z0-9 ,-]*$",message="only alphanumeric")])

class getid(FlaskForm):
    PatientId = StringField('Patient ID*', validators=[InputRequired(),Length(max=9,min=9,message="SSN ID must be of 9 digits numeric"),Regexp(regex="[0-9]*$",message="Must be numeric")])

class DeletePatient(FlaskForm):
    PatientId = StringField('PatientID', validators=[InputRequired(),Length(max=9,min=9,message="PatientsID must be of 9 digits numeric"),Regexp(regex="^[0-9]*",message="Must be numeric")])


class SearchForPatient(FlaskForm):
    PatientId = StringField('PatientID', validators=[InputRequired(),Length(max=9,min=9,message="PatientsID must be of 9 digits numeric"),Regexp(regex="^[0-9]*",message="Must be numeric")])

class Billing(FlaskForm):
    PatientId = StringField('PatientID', validators=[InputRequired(),Length(max=9,min=9,message="PatientsID must be of 9 digits numeric"),Regexp(regex="^[0-9]*",message="Must be numeric")])
#-------------------------------------------------------Pharmacy------------------------------------------------------------------#

class PharmaViewPatientsDetail(FlaskForm):
    PatientId = StringField('PatientID', validators=[InputRequired(),Length(max=9,min=9,message="PatientsID must be of 9 digits numeric"),Regexp(regex="^[0-9]*",message="Must be numeric")])

class IssueMedicines(FlaskForm):
    MedicineName = StringField('MedicineName', validators=[InputRequired(),Regexp(regex="[A-Za-z]*")])

class GetQuantity(FlaskForm):
    Quantity = StringField('Quantity', validators=[InputRequired(),Regexp(regex="[0-9]*",message="somthing")])

class updatemrecord(FlaskForm):
    updatebutton = SubmitField('Update')

#---------------------------------------------------------Diagnostics--------------------------------------------------------------------------#
class Diagnostic(FlaskForm):
    PatientId = StringField('PatientID', validators=[InputRequired(),Length(max=9,min=9,message="PatientsID must be of 9 digits numeric"),Regexp(regex="^[0-9]*",message="Must be numeric")])

class AddDiagnostics(FlaskForm):
    diagnostictest=SelectField('Diagnostic Test', choices=[('Select', 'Select')])