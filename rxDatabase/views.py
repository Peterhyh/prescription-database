from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Record
from . import db                                                 


views=Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def findrx():
    patient_name = request.args.get("fname")
    rec={}
    if patient_name:
        rec=Record.query.filter(Record.patient_name.like(f'%{patient_name}%')).first()
    return render_template('findrx.html', user=current_user, rec=rec, fname=patient_name)


@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.findrx'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Login email does not exist', category='error')
        
    return render_template('login.html', user=current_user)


@views.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))


@views.route("/sign-up", methods=["GET","POST"])                         
def sign_up():
    if request.method == "POST":                                        
        email = request.form.get('email')                              
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:        
            flash('User already exist.', category='error') 
        elif len(email) < 4:                                            
            flash('Your email must be at least than 4 characters', category='error')
        elif len(firstName) < 2:
            flash('Your first name must be at least 2 characters', category='error')
        elif password1 != password2:
            flash('Your password must match!', category='error')
        elif len(password1) < 7:
            flash('Your password must be at least 7 characters!', category='error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))  
            db.session.add(new_user)                                  
            db.session.commit()                                     
            login_user(new_user, remember= True)                          
            flash('Your account has been created!', category='success')
            return redirect(url_for('views.findrx'))                          
    return render_template("sign_up.html", user=current_user)


@views.route("/newrx", methods=["GET","POST"])
@login_required
def newrx():
    form = request.form
    if request.method == "POST":
        prescription_number = request.form.get("prescription_number")
        patient_name = request.form.get("patient_name")
        date_of_birth = request.form.get("date_of_birth")
        address = request.form.get("address")
        drug_name = request.form.get("drug_name")
        date_prescribed= request.form.get("date_prescribed")

        
        if len(prescription_number) != 4:
            flash("There must 4 characters.", category="error")
        if len(patient_name) < 1:
           flash("Patient's name is required", category="error")
        if len(address) < 4:
            flash("Address must be at least 4 characters", category="error")
        if len(date_of_birth) < 8:
            flash("Date of birth must be valid (e.g. MM/DD/YYYY)", category="error")     
        if len(drug_name) < 1:
            flash("Drug name is required.", category="error")
        if len(date_prescribed) < 8:
            flash("Prescription date must be valid (e.g. MM/DD/YYYY)", category="error")
        else:
            new_patient = Record(
                prescription_number=form['prescription_number'], 
                user_id=current_user.id,
                patient_name=patient_name,
                date_of_birth=date_of_birth,
                address=address,
                date_prescribed=date_prescribed,
                drug_name=drug_name
                )
            db.session.add(new_patient)
            db.session.commit()
            flash("Patient's prescription has been stored successfully!", category="success")
            return redirect(url_for('views.newrx'))
    return render_template("newrx.html", user=current_user)