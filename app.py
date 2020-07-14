from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import Length, DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = "123"

class UserForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def hello():
    form = UserForm()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('form.html', form=form)

@app.route('/success')
def success():
    return 'Success!'

if __name__ == '__main__':
    app.run(debug=True)