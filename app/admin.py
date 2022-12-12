from flask import Flask
from flask_admin import Admin,BaseView,expose
from app import app,db,dao
from flask_admin.contrib.sqla import ModelView
from app.models import Phong, LoaiPhong, KhachHang, ChiTietPhieuDat, HoaDon,UserRoleEnum
from flask_login import current_user,logout_user
from flask import request
from datetime import datetime

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedEmployeeModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class phongModelView(AuthenticatedModelView):
    column_searchable_list = ['tenPhong','ghiChu']
    column_filters = ['tenPhong']
    column_exclude_list = ['Image']
    column_labels = {
        'tenPhong':'Tên Phòng',
        'tinhTrang':'Tình Trạng',
        'Image':'Image',

    }
class loaiPhongModelView(AuthenticatedModelView):
    column_searchable_list = ['tenLoaiPhong']

class EmployeeView(AuthenticatedEmployeeModelView):
        can_delete = False
class chiTietPhieuDatModelView(EmployeeView):
    column_searchable_list = ['id']

class chiTietHoaDonModelView(EmployeeView):
    column_searchable_list = ['id']
class khachHangModelView(EmployeeView):
    column_searchable_list = ['name']
    column_filters = ['name']
    column_exclude_list = ['password', 'avatar', 'active', 'username']
    column_labels = {
        'name':'Tên',
        'email':'Email',
        'diaChi':'Địa chỉ',
        'cmnd':'CMND'

    }

class StatsView(BaseView):
    @expose('/')
    def __index__(seft):
        kw = request.args.get('kw')
        year = request.args.get('year', datetime.now().year)
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        return  seft.render('admin/stats.html',
                            kw = kw,
                            from_date = from_date,
                            to_date = to_date,
                            month_stats = dao.product_month_stats(year = year),
                            stats = dao.phong_stats())

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

admin = Admin(app=app, name='Quản trị khách sạn', template_mode='bootstrap4')
admin.add_view(khachHangModelView(KhachHang, db.session, name = "khách hàng"))
admin.add_view(loaiPhongModelView(LoaiPhong,db.session,name='Loại Phòng'))
admin.add_view(EmployeeView(Phong, db.session,name='Phòng'))
admin.add_view(EmployeeView(ChiTietPhieuDat, db.session, name = "Chi tiết phiếu đặt"))
admin.add_view(EmployeeView(HoaDon, db.session, name = "Hóa đơn"))
admin.add_view(StatsView(name='Thống kê'))