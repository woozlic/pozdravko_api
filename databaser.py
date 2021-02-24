from sqlalchemy.orm import sessionmaker
from database_setup import Card, Base, engine, Category, User, VkUser, Likes
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import update
from werkzeug.security import generate_password_hash
from datetime import date
from flask import url_for
from config import HOST
import datetime

def get_date():
    # YYYY-MM-DD
    return date.today()


def date_to_str(date: datetime.date, format_out='%Y-%m-%d'):
    """
    Returns str for input datetime.date
    :param date: datetime.time object
    :param format_out: format of output string
    :return: String like
    """
    if date is None:
        return None
    else:
        return date.strftime(format_out)


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


def delete_category(name):
    category = select_category(name)
    if category:
        session.delete(category)
        session.commit()
        return True
    else:
        print("Не удалось удалить категорию")
        return False


def select_category(name):
    try:
        category = session.query(Category).filter_by(category_name=name).one()
        return category.category_name
    except NoResultFound:
        print("Категории {name} не существует")
        return False


def select_categories():
    categories = session.query(Category).all()
    return categories


def create_category(name):
    category = select_category(name)
    if category:
        return False
    else:
        new_category = Category(category_name=name)
        session.add(new_category)
        session.commit()
        print(f"Категория {name} была создана")
        return True


def select_cards():
    cards = session.query(Card).all()

    if cards:
        lst = [{"id": c.id, "img": HOST+url_for('main.uploaded_file', category=c.category, filename=c.img),
                "category": c.category, "date": date_to_str(c.date),
                "vkusers": [i.vk_id for i in c.vkusers]} for c in cards]
        lst.sort(key=lambda x: x['id'], reverse=True)
        return lst
    else:
        return []


def create_card(img, category):
    card = Card(img=img, category=category, date=get_date())
    session.add(card)
    session.commit()


def delete_card(id):
    card = select_card_by_id(id)
    if card:
        session.delete(card)
        session.commit()
        return True
    else:
        print("Невозможно удалить открытку, ее нет")
        return False


def delete_all_cards():
    cards = session.query(Card).all()
    for card in cards:
        session.delete(card)
    session.commit()
    print("Все открытки были удалены")
    return True


def select_cards_by_category(category):
    cards = session.query(Card).filter_by(category=category).all()
    if cards:
        return [{"id": c.id, "img": c.img, "category": c.category, "date": c.date} for c in cards]
    else:
        return []


def select_card_by_id(id):
    try:
        card = session.query(Card).filter_by(id=id).one()
        return {"id": card.id, "img": card.img, "category": card.category, "date": card.date}
    except NoResultFound:
        print(f"Открытки с id={id} не существует")
        return {}


def get_user(username):
    try:
        return session.query(User).filter_by(username=username).one()
    except NoResultFound:
        return None


def get_user_by_id(id):
    return session.query(User).filter_by(id=id).one()


def create_user(username, password):
    user = get_user(username)
    if user:
        print(f'Пользователь с ником {username} уже существует')
    else:
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
        session.add(new_user)
        session.commit()
        print(f'Создан пользователь с ником {username}')


def add_or_remove_like(vk_id, img_id):
    card = session.query(Card).filter_by(id=img_id).one()
    try:
        user_exists = session.query(VkUser).filter_by(vk_id=vk_id).one()
        if card.vkusers:
            likes = [i.vk_id for i in card.vkusers]
            # print(likes)
            if vk_id in likes:
                print('Пользователь уже лайкнул эту запись')
                card.vkusers.remove(user_exists)
            else:
                card.vkusers.append(user_exists)
        else:
            card.vkusers.append(user_exists)
    except NoResultFound:
        user = VkUser(vk_id=vk_id)
        card.vkusers.append(user)
        session.add(user)
    session.commit()
    return True


def get_likes(img_id):
    try:
        card = session.query(Card).filter_by(id=img_id).one()
        if card.vkusers:
            likes = [i.vk_id for i in card.vkusers]
            return likes
        else:
            return []
    except NoResultFound:
        print('Открытка не найдена')
        return False

