from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileAllowed,FileRequired
from app.models import User, BusinessUnit
from flask_login import login_user, logout_user, current_user, login_required
from app import db

def BU_NAME_choices():
    bu = BusinessUnit.query.filter_by(user_id=current_user.id)
    return bu

def Time_alert_choices():
    time_to_alert = [10,15,20,25,30]
    return time_to_alert


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    # recaptcha = RecaptchaField()
    submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email',validators=[Email()])
    about = TextAreaField('About me', validators=[Length(min=0, max=140)])
    line = StringField('line id')
    mobile = StringField('Mobile Number')
    facebook = StringField('facebook')
    role = StringField('Role')
    pic = FileField('Upload Chemical Structure',validators=[FileAllowed('jpg','png'), FileRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Register')
    # recaptcha = RecaptchaField()
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')





class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Request Password Reset')



class EmptyForm(FlaskForm):
    title=StringField('title')
    gps=StringField('GPS')
    body=CKEditorField('บทความ')
    image=StringField('Url Image',render_kw={"placeholder": "http://example.image.jpg"})
    pic = FileField('Upload Chemical Structure',validators=[FileAllowed('jpg','png'), FileRequired()])
    submit = SubmitField('Submit')

class NodeForm(FlaskForm):
    api_key = StringField('API KEY')
    mac = StringField('MAC ADDR')
    bu_name = QuerySelectField('Business unit name',
                               query_factory=BU_NAME_choices)
    node_name = StringField('Node ID(PE)')
    gps_latitude=StringField('GPS latitude')
    gps_longtitude = StringField('GPS longtitude')
    image_node =FileField('Upload Node Image',validators=[FileAllowed('jpg','png')])
    sensor_name = StringField('Sensor Name')
    imei=StringField('Sensor IMEI')

    time_alert = QuerySelectField('ระยะเวลาที่จะแจ้งเตือน(นาที)',
                               query_factory=Time_alert_choices)
    tank_size = StringField('Tank Size(Litre)')
    current_Height = StringField('Current Liquid Hight(Metre)')
    current_Volumn = StringField('Current Liquid Volume(Litre)')
    
    temp_hight_alert=StringField('Temperature Hight level Alert(C)')
    temp_low_alert = StringField("Temperature Low level Alert(C)")

    hu_hight_alert =StringField('Humidity Hight level Alert(%RH)')
    hu_low_alert =StringField('Humidity low level Alert(%RH)')


    high_level_alert = StringField('High level Alert(Litre)')
    low_level_alert = StringField('Low level Alert(Litre)')
    maximum_rise_alert = StringField('High level rise Alert(Metre/time)')
    maximum_drop_alert = StringField('High drop Alert(Metre/time)')
    submit = SubmitField('Submit')