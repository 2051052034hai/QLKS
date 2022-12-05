from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app
from datetime import datetime

# class nav_category(db.Model):
#     name = Column

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class LoaiPhong(BaseModel):
    name = Column(String(50), nullable=False)
    phong = relationship('Phong', backref='LoaiPhong', lazy=False)

    def __str__(self):
            return self.name

class Phong(BaseModel):
    tenPhong = Column(String(50), nullable=False)
    tinhTrang = Column(Boolean, default=True)
    maLoaiPhong = Column(Integer, ForeignKey(LoaiPhong.id), nullable=False)
    # maPhong = relationship('PhieuDatPhong', backref='Phong', lazy=False)
    donGia = Column(Float, default=0)
    image = Column(String(100))
    moTa = Column(Text)

    def __str__(self):
        return self.name
if __name__ == '__main__':
    with app.app_context():
         #db.create_all()
        # lp1 = LoaiPhong(name='Phòng gia đình')
        # lp2 = LoaiPhong(name='Phòng cổ điển')
        # lp3 = LoaiPhong(name='Phòng cơ sở')
        # lp4 = LoaiPhong(name='Phòng điều hành')
        #
        # db.session.add_all([lp1, lp2, lp3])
        # db.session.commit()

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

        # db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)

        db.session.commit()
