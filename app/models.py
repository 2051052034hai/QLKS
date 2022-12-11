from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, Enum, DateTime,BigInteger
from sqlalchemy.orm import relationship, backref
from app import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin

class baseModel(db.Model):
    __abstract__ = True
    id=Column(Integer,primary_key=True,autoincrement=True)

class UserRoleEnum(UserEnum):
    GUEST=1
    EMPLOYEE=2
    ADMIN=3

class LoaiPhong(baseModel):
    tenLoaiPhong=Column(String(50),default=False)
    donGia=Column(BigInteger,default=True)
    lp_p=relationship('Phong',backref='LoaiPhong',lazy=False)


class Phong(baseModel):
    tenPhong=Column(String(50),default=False)
    tinhTrang=Column(Boolean,default=True)
    ghiChu=Column(String(300))
    maLoaiPhong=Column(Integer,ForeignKey(LoaiPhong.id))
    image = Column(String(100))
    lp_slptpd = relationship('SoLuongPhongTrongPhieuDat', backref='Phong', lazy=False)

class User(baseModel, UserMixin):
    name=Column(String(50),default=False)
    username=Column(String(50),default=False)
    password=Column(String(50),default=False)
    email=Column(String(50))
    diaChi=Column(String(100))
    cmnd=Column(String(20))
    avatar=Column(String(100))
    active=Column(Boolean,default=True)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.GUEST)

class LoaiKhach(baseModel):
    tenLoaiKhach=Column(String(50),default=False)
    lk_k=relationship('KhachHang',backref='LoaiKhach',lazy=False)
class KhachHang(User):
    maLoaiKhach=Column(Integer,ForeignKey(LoaiKhach.id))
    kh_pdp=relationship('PhieuDatPhong',backref='KhachHang',lazy=False)
class PhieuDatPhong(baseModel):
    ngayNhanPhong=Column(DateTime,default=datetime.now())
    ngayTraPhong=Column(DateTime)
    pdp_slptpd=relationship('SoLuongPhongTrongPhieuDat',backref='PhieuDatPhong',lazy=False)
    pdp_hd=relationship('HoaDon',backref='PhieuDatPhong',lazy=False)
    maKhachHang=Column(Integer,ForeignKey(KhachHang.id))

class SoLuongPhongTrongPhieuDat(baseModel):
    soLuongPhong=Column(Integer,default=False)
    malOaiPhong=Column(Integer,ForeignKey(Phong.id))
    maPhieuDat=Column(Integer,ForeignKey(PhieuDatPhong.id))


class HoaDon(baseModel):
    soNgayThue=Column(Integer,default=False)
    donGia=Column(BigInteger,default=False)
    tongTien=Column(BigInteger,default=False)
    maPhieuDat=Column(Integer,ForeignKey(PhieuDatPhong.id),)
    ngayThanhToan=Column(DateTime)


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()

        import hashlib

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        U = User(name='VA', email='dasdfjosa@gmail.com', username='admin', password=password,
                 diaChi='DFJSAFOIASJFOIAS',
                 cmnd='345345345',avatar='fdsfasfasfasfsafsa',
                 user_role=UserRoleEnum.ADMIN, active=1)

        db.session.add(U)
        db.session.commit()

