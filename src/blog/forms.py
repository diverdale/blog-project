from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField


class AddForm(FlaskForm):

    post_title = StringField('Title: ')
    post_content = TextAreaField('Body', render_kw={'rows': 10})
    submit = SubmitField('Submit')
