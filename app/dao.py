from app.models import LoaiPhong, Phong,User, KhachHang
from app import db,app
from  flask import  request
from flask_login import current_user
import hashlib

def load_LoaiPhong():
    return LoaiPhong.query.all()


def load_Phong(ma_lp=None, lp=None, page = 1):
    query = Phong.query.filter(Phong.tinhTrang.__eq__(True))

    if ma_lp:
        query = query.filter(Phong.maLoaiPhong.__eq__(ma_lp))

    if lp:
        query = query.filter(Phong.maLoaiPhong.__eq__(lp))

    page_size = app.config['PAGE_SIZE']
    start = (page-1) * page_size
    end = start + page_size

    return query.slice(start, end).all()

# Đây là hàm đếm số luượng phòng có trong cơ sở dữ liệu
def count_phong():
    return Phong.query.filter(Phong.tinhTrang.__eq__(True)).count()
def get_phong_by_id(phong_id):
    return Phong.query.get(phong_id)

def auth_user(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)

def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = KhachHang(name = name.strip(),
                username = username.strip(),
                password = password,
                email = kwargs.get('email'),
                diaChi = kwargs.get('diaChi'),
                cmnd = kwargs.get('cmnd'),
                avatar = kwargs.get('avatar'))
    db.session.add(user)
    db.session.commit()

