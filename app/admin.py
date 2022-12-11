from flask import Flask
from flask_admin import Admin
from app import app,db
from flask_admin.contrib.sqla import ModelView
from app.models import Phong, LoaiPhong, KhachHang, SoLuongPhongTrongPhieuDat, HoaDon
class phongModelView(ModelView):
    column_searchable_list = ['tenPhong','ghiChu']
    column_filters = ['tenPhong']
    column_exclude_list = ['Image']
    column_labels = {
        'tenPhong':'Tên Phòng',
        'tinhTrang':'Tình Trạng',
        'Image':'Image',

    }



admin = Admin(app=app, name='Quản trị khách sạn', template_mode='bootstrap4')
admin.add_view(phongModelView(Phong, db.session,name='Phòng'))
admin.add_view(ModelView(LoaiPhong,db.session,name='Loại Phòng'))
admin.add_view(ModelView(KhachHang, db.session, name = "khách hàng"))
admin.add_view(ModelView(SoLuongPhongTrongPhieuDat, db.session, name = "slptpd"))
admin.add_view(ModelView(HoaDon, db.session, name = "hoa don"))
