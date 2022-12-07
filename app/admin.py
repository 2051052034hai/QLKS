from flask import Flask
from flask_admin import Admin
from app import app,db
from flask_admin.contrib.sqla import ModelView
from app.models import Phong, LoaiPhong
class phongModelView(ModelView):
    column_searchable_list = ['tenPhong','moTa']
    column_filters = ['tenPhong','donGia']
    column_exclude_list = ['Image']
    column_labels = {
        'tenPhong':'Tên Phòng',
        'tinhTrang':'Tình Trạng',
        'donGia':'Đơn Giá',
        'Image':'Image',
        'moTa':'Mô Tả'
    }



admin = Admin(app=app, name='Quản trị khách sạn', template_mode='bootstrap4')
admin.add_view(phongModelView(Phong, db.session,name='Phòng'))
admin.add_view(ModelView(LoaiPhong,db.session,name='Loại Phòng'))