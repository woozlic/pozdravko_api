from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
from databaser import *
from forms import UploadCardsForm, AddCategoryForm
from werkzeug.utils import secure_filename
import os
from config import UPLOAD_FOLDER, allowed_file
import json

version = "/api/v1.0"

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', user=current_user)


@main.route('/apis')
def show_apis():
    return render_template('show_apis.html', user=current_user)

@main.route('/add', methods=['GET'])
@login_required
def add():
    if request.method == 'GET':
        return render_template('add.html', user=current_user)


@main.route('/add/category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = AddCategoryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            category = request.form['category']
            if category:
                if create_category(category):
                    flash('Категория успешно добавлена')
                else:
                    flash('Категория уже существует')
            else:
                flash('Поле не должно быть пустым')

    return render_template('add_category.html', form=form, user=current_user)


@main.route('/add/cards', methods=['POST', 'GET'])
@login_required
def add_cards():
    form = UploadCardsForm.new()
    if request.method == 'POST':
        if form.validate_on_submit():
            files_filenames = []
            category = request.form['sel']

            if not os.path.exists(os.path.join(UPLOAD_FOLDER, category)):
                os.makedirs(os.path.join(UPLOAD_FOLDER, category))

            if 'files' not in request.files:
                flash('Вы не выбрали файлы')
                return redirect(url_for('main.add_cards'))
            files = request.files.getlist('files')
            for file in files:
                # file_filename = secure_filename(file.filename)  # не работает с кириллицей
                file_filename = file.filename
                print(file_filename)
                if file and allowed_file(file_filename):
                    folder = os.path.join(UPLOAD_FOLDER, category)
                    file.save(os.path.join(folder, file_filename))
                    files_filenames.append(file_filename)

                    card = create_card(file_filename, category)
                else:
                    flash(f'У файла {file_filename} недопустимое расширение')
            count_files = len(files_filenames)
            flash(f'Вы успешно загрузили {count_files} открыток')
        else:
            flash(form.errors)
    return render_template('upload_cards.html', user=current_user, form=form)


@main.route('/uploads/<category>/<filename>')
def uploaded_file(category, filename):
    category_and_name = f'{category}/{filename}'
    return send_from_directory(UPLOAD_FOLDER, category_and_name)


@main.route(f'{version}/cards')
def get_cards():
    """
    This function just returns all cards
    :return:
    """
    cards = select_cards()
    return render_template('all_cards.html', cards=cards, user=current_user)


@main.route(f'{version}/cards.js')
def get_cards_js():
    """
    This function just returns all cards
    :return:
    """
    cards = json.dumps(select_cards(), ensure_ascii=False, indent=4)
    return cards


@main.route(f'{version}/card/<int:id>')
def get_card_by_id(id):
    """
    This function just returns all cards
    :return:
    """
    card = select_card_by_id(id)
    return render_template('index.html', card=card)


@main.route(f'{version}/card/<int:id>.js')
def get_card_by_id_js(id):
    """
    This function just returns all cards
    :return:
    """
    card = jsonify(select_card_by_id(id))
    return card


@main.route(f'{version}/cards/<string:category>')
def get_cards_by_category(category):
    """
    This function just returns all cards
    :return:
    """
    cards = select_cards_by_category(category)
    return render_template('index.html', cards=cards)


@main.route(f'{version}/cards/<string:category>.js')
def get_cards_by_category_js(category):
    """
    This function just returns all cards
    :return:
    """
    cards = jsonify(select_cards_by_category(category))
    return cards
