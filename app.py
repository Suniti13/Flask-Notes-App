from flask import Flask, render_template, url_for, redirect, flash
from wtforms import Form, StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import Length, DataRequired, Email
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "123"



@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data=='example@123.com' and form.password.data=='asdf':
            flash('Succesfully Logged In!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessfull. Please check email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)