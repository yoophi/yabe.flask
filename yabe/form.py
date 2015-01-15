from wtforms import Form, TextField, DateTimeField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import Length, required

class AppointmentForm(Form):
    title = TextField('Title', [Length(max=255)])
    start = DateTimeField('Start', [required()])
    end = DateTimeField('End')
    allday = BooleanField('All Day')
    location = TextField('Location', [Length(max=255)])
    description = TextAreaField('Description')


class LoginForm(Form):
    username = TextField('Username', [required()])
    password = PasswordField('Password', [required()])

