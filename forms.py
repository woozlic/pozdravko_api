from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, MultipleFileField, StringField, PasswordField
from wtforms.validators import Required
from databaser import select_categories


class UploadCardsForm(FlaskForm):

    sel = SelectField("Категория: ")
    files = MultipleFileField('files')

    @classmethod
    def new(cls):
        form = cls()

        form.sel.choices = [(i.category_name, i.category_name) for i in select_categories()]
        return form


class AddCategoryForm(FlaskForm):

    category = StringField('Категория')


class LoginForm(FlaskForm):

    username = StringField('Логин')
    password = PasswordField('Пароль')
