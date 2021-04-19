from wtforms import TextField, SubmitField,PasswordField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Email
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators

class Addproducts(Form):
    name = StringField('Name', validators=[InputRequired()])
    price = DecimalField('Price', validators=[InputRequired()])
    discount = IntegerField('Discount', validators=[InputRequired()])
    stock = IntegerField('Stock', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])

    image_1 = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

