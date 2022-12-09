from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRoleEnum(UserEnum):
    CLIENT = 0
    EMPLOYEE = 1
    ADMIN = 2


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.CLIENT)

    def __str__(self):
        return self.name


class BaseModel2(db.Model):
    __abstract__ = True
    id = Column(String(50), primary_key=True)


class LoaiPhong(BaseModel):
    name = Column(String(50), nullable=False)
    phong = relationship('Phong', backref='LoaiPhong', lazy=False)

    def __str__(self):
        return self.name


class Phong(BaseModel):
    tenPhong = Column(String(50), nullable=False)
    tinhTrang = Column(Boolean, default=True)
    maLoaiPhong = Column(Integer, ForeignKey(LoaiPhong.id), nullable=False)
    P_PDP = relationship('PhieuDatPhong', backref='Phong', lazy=False)
    donGia = Column(Float, default=0)
    image = Column(String(100))
    moTa = Column(Text)

    def __str__(self):
        return self.tenPhong


class PhieuDatPhong(BaseModel):
    ngayNhanPhong = Column(DateTime, default=datetime.now())
    ngayTraPhong = Column(DateTime)
    maPhong = Column(Integer, ForeignKey(Phong.id), nullable=False)
    PDP_CTPD = relationship('ChiTietPhieuDat', backref='PhieuDatPhong', lazy=False)


class LoaiKhach(BaseModel):
    tenLoaiKhach = Column(String(30))
    khachhang = relationship('KhachHang', backref='LoaiKhach', lazy=False)

    def __str__(self):
        return self.tenLoaiKhach


class KhachHang(User):
    diaChi = Column(String(100))
    cmnd = Column(String(20))
    maLoaiKhach = Column(Integer, ForeignKey(LoaiKhach.id),nullable = False, default = 1 )
    KH_CTPD = relationship('ChiTietPhieuDat', backref='KhachHang', lazy=False)

    def __str__(self):
        return self.tenKhachHang


class ChiTietPhieuDat(BaseModel):
    maKhachHang = Column(Integer, ForeignKey(KhachHang.id), nullable=False, primary_key=True)
    maPhieuDat = Column(Integer, ForeignKey(PhieuDatPhong.id), nullable=False, primary_key=True)
    CTPD_CTHD = relationship('ChiTietHoaDon', backref='ChiTietPhieuDat', lazy=False)


class HoaDon(BaseModel):
    ngayThanhToan = Column(DateTime, default=datetime.now())
    triGia = Column(Float, nullable=False)
    HD_CTHD = relationship('ChiTietHoaDon', backref='HoaDon', lazy=False)


class ChiTietHoaDon(BaseModel):
    soNgayThue = Column(Integer, default=False)
    donGia = Column(Float, nullable=False)
    tongTien = Column(Float, default=donGia * soNgayThue)
    maHoaDon = Column(Integer, ForeignKey(HoaDon.id), nullable=False)
    maChiTietPhieuDat = Column(Integer, ForeignKey(ChiTietPhieuDat.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
         # db.create_all()
        lp1 = LoaiPhong(name='Phòng gia đình')
        lp2 = LoaiPhong(name='Phòng cổ điển')
        lp3 = LoaiPhong(name='Phòng cơ sở')
        lp4 = LoaiPhong(name='Phòng điều hành')

        db.session.add_all([lp1, lp2, lp3])
        db.session.commit()

        p1 = Phong(tenPhong="Phòng gia đình", moTa='Thoải mái & ấm cúng, có thể chứa tối đa 2 người.',
                   donGia=3000000,
                   image='https://res.cloudinary.com/dcteoaxmv/image/upload/v1670237774/Family_tviwwj.jpg',
                   maLoaiPhong=1)
        p2 = Phong(tenPhong="Phòng cơ sở", moTa='Thoải mái & ấm cúng, có thể chứa tối đa 2 người.',
                   donGia=4000000,
                   image='https://res.cloudinary.com/dcteoaxmv/image/upload/v1670237774/Family_tviwwj.jpg',
                   maLoaiPhong=3)

        p3 = Phong(tenPhong="Phòng cổ điển", moTa='Thoải mái & ấm cúng, có thể chứa tối đa 2 người.',
                   donGia=4000000,
                   image='https://res.cloudinary.com/dcteoaxmv/image/upload/v1670237774/Family_tviwwj.jpg',
                   maLoaiPhong=2)

        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.commit()

    # lk1 = LoaiKhach(tenLoaiKhach = "nuoc ngoai")
    # lk2 = LoaiKhach(tenLoaiKhach = "trong nuoc")
    # db.session.add_all([lk1, lk2])
    # db.session.commit()

    # kh1 = KhachHang(tenKhachHang = "nguyen van a", diaChi = "tay ninh", cmnd = "123456", maLoaiKhach = 1)
    # kh2= KhachHang(tenKhachHang="le viet anh", diaChi="ninh binh", cmnd="15856", maLoaiKhach=2)
    # kh3 = KhachHang(tenKhachHang="tran thanh hai", diaChi="ha noi", cmnd="15856", maLoaiKhach=1)
    #
    # db.session.add(kh1)
    # db.session.add(kh2)
    # db.session.add(kh3)
    # db.session.commit()

    # import hashlib
    # password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
    # U= User(name='VA1', email='dasdfjosa@gmail.com',username='admin',password=password,user_role=UserRoleEnum.ADMIN,active=1)
    # db.session.add(U)
    # db.session.commit()
