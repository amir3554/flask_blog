from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
import wtforms
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField


class ArticleForm(FlaskForm):
    title = wtforms.StringField("Title", validators=[DataRequired(), Length(min=5, max=255)])
    content = CKEditorField("Content", validators=[DataRequired(), Length(min=100, max=10000)])
    image = FileField("Image", validators=[FileAllowed(['jpg', 'png'])])
    existing_image = wtforms.HiddenField()
    submit = wtforms.SubmitField("Submit")
    