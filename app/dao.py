from app.models import LoaiPhong, Phong,User
from app import db,app,dao
from flask_login import current_user
import hashlib

def load_LoaiPhong():
    return LoaiPhong.query.all()


def load_Phong(ma_lp=None, kw=None):
    query = Phong.query

    if ma_lp:
        query = query.filter(Phong.maLoaiPhong.__eq__(ma_lp))

    if kw:
        query = query.filter(Phong.tenPhong.contains(kw))

    return query.all()

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)
