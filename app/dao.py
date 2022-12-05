from app.models import LoaiPhong, Phong
from app import db



def load_LoaiPhong():
    return LoaiPhong.query.all()


def load_Phong(ma_lp=None, kw=None):
    query = Phong.query

    if ma_lp:
        query = query.filter(Phong.maLoaiPhong.__eq__(ma_lp))

    if kw:
        query = query.filter(Phong.tenPhong.contains(kw))

    return query.all()


