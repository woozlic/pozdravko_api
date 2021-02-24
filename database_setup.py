import sys
# для настройки баз данных
from sqlalchemy import *
from sqlalchemy.exc import ProgrammingError
# для определения таблицы и модели
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database, database_exists
from flask_login import UserMixin

# для создания отношений между таблицами
from sqlalchemy.orm import relationship

from config import db_user, db_password, db_host

url = "mysql://{0}:{1}@{2}".format(db_user, db_password, db_host)
db = url + "/cards?charset=utf8mb4"

# создание экземпляра declarative_base
Base = declarative_base()

# здесь добавим классы

# создает экземпляр create_engine в конце файла
# try:
#     engine = create_engine("mysql://root:faqxakep@localhost")
#     engine.execute("CREATE DATABASE cards")
#     engine.execute("USE cards")
# except ProgrammingError:
if not database_exists(db):
    create_database(db)
engine = create_engine(db)

if database_exists(engine.url):
    print("Database exists. Setup is succeed")


class Card(Base):
    __tablename__ = 'card'

    id = Column(Integer, primary_key=True)
    img = Column(String(250), nullable=False)
    category = Column(String(250), ForeignKey('category.id'))
    date = Column(Date)
    vkusers = relationship('VkUser', secondary='likes')


class VkUser(Base):
    __tablename__ = 'vkuser'

    id = Column(Integer, primary_key=True)
    vk_id = Column(String(40))
    cards = relationship('Card', secondary='likes')


class Likes(Base):
    __tablename__ = 'likes'

    card_id = Column(Integer, ForeignKey('card.id'), primary_key=True)
    vk_id = Column(Integer, ForeignKey('vkuser.id'), primary_key=True)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    category_name = Column(String(250), nullable=False)
    card = relationship('Card')


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    password = Column(String(100))


# class Likes(Base):
#     __tablename__ = "Likes"
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(String(25), nullable=False)
#     card_id =

Base.metadata.create_all(engine)
