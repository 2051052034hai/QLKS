import math

import cloudinary.uploader
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from app import app, dao, login
from flask_login import login_user, logout_user, login_required, current_user
from app.decorators import annonymous_user
from app.admin import *


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/phong/<int:phong_id>")
def phong_detail(phong_id):
    phong = dao.get_phong_by_id(phong_id)

    return render_template('phong_detail.html', p=phong)


@app.route('/user-login', methods=['get', 'post'])
def login_my_user():
    err_msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:

            login_user(user=user)

            next = request.args.get('next', 'index')
            return redirect(url_for(next))
        else:
            err_msg = "username hoặc password không chính xác!"
    return render_template('login.html', err_msg=err_msg)


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('login_my_user'))


@app.context_processor
def common_response():
    ma_lp = request.args.get('maLoaiPhong')
    lp_id = request.args.get('loaiPhong_id')
    page = request.args.get('page', 1)
    phong = dao.load_Phong(ma_lp=ma_lp, lp=lp_id, page=int(page))
    counter = dao.count_phong()
    return {
        'phong': phong,
        'pages': math.ceil(counter / app.config['PAGE_SIZE']),
        'loaiphong': dao.load_LoaiPhong(),
        'cart_stats': dao.count_cart(session.get('cart'))
    }


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('Email')
        diaChi = request.form.get('adress')
        cmnd = request.form.get('cmnd')
        cofirm = request.form.get('cofirm')
        avatar_path = None
        try:
            if password.strip().__eq__(cofirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                    dao.add_user(name=name, username=username,
                                 password=password, email=email,
                                 diaChi=diaChi, cmnd=cmnd,
                                 avatar=avatar_path)
                return redirect(url_for('login_my_user'))
            else:
                err_msg = "Mật khẩu không chính xác!"

        except Exception as ex:
            err_msg = "Hệ thống đang có lỗi" + str(ex)

    return render_template('register.html', err_msg=err_msg)


@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    data = request.json
    err_msg = ""
    id = str(data.get('id'))
    tenPhong = data.get('tenPhong')
    donGia = data.get('donGia')
    soNgayThue = data.get('soNgayThue')
    ngayNhanPhong = data.get('ngayNhanPhong')
    ngayTraPhong = data.get('ngayTraPhong')
    soLuong = data.get('soLuongKhach')
    loaiKhach = data.get('loaiKhach')
    cart = session.get('cart')
    tienThue = ""
    if not cart:
        cart = {}

    if id in cart:
        err_msg = "Bạn đã đặt phòng này rồi !"
    else:
        cart[id] = {
            'id': id,
            'tenPhong': tenPhong,
            'donGia': donGia,
            'ngayNhanPhong': ngayNhanPhong,
            'ngayTraPhong': ngayTraPhong,
            'soNgayThue': soNgayThue,
            'soLuongKhach': soLuong,
            'loaiKhach': loaiKhach,
            'tienThue': tienThue,
        }
    session['cart'] = cart

    return jsonify(dao.count_cart(cart))


@app.route('/cart')
def cart():
    return render_template('cart.html', stats=dao.count_cart(session.get('cart')))


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/api/pay', methods=['post'])
def pay():
    try:
        dao.add_hoaDon(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})
