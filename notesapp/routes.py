from flask import render_template, url_for, redirect, flash
from notesapp import app, db, bcrypt
from notesapp.models import User, Note
from notesapp.forms import RegisterForm, LoginForm, AddNoteForm
from flask_login import login_user, current_user, logout_user

@app.route('/')
def landing():
    return render_template('landing.html', title='Notes')

@app.route('/home')
def home():
    return render_template('home.html', title='Home', prevnotes=Note.query.filter_by(author=current_user))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to LogIn', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessfull. Please check email or password', 'danger')
    return render_template('login.html', form=form, title='LogIn')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('landing'))

@app.route('/note/new', methods=['GET', 'POST'])
def addnote():
    form = AddNoteForm()
    if form.validate_on_submit():
        newNote = Note(title=form.title.data, content=form.body.data, author=current_user)
        db.session.add(newNote)
        db.session.commit()
        flash("Added")
        return redirect( url_for('home') )
    return render_template('addnote.html', form=form, title='Add Note')

@app.route('/note/<int:note_id>', methods=['GET', 'POST'])
def note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('note.html', note=note, title=note.title)
