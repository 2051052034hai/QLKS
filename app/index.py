import math

from flask import Flask, render_template, request, redirect
from app import app, dao,login
from flask_login import login_user, logout_user, login_required, current_user
from app.decorators import annonymous_user
from app.admin import *


@app.route("/")
def index():
    ma_lp = request.args.get('maLoaiPhong')
    lp_id = request.args.get('loaiPhong_id')
    page = request.args.get('page', 1)
    phong = dao.load_Phong(ma_lp=ma_lp, lp = lp_id, page= int(page))
    loaiphong = dao.load_LoaiPhong()
    couter = dao.count_phong()
    return render_template('index.html',
                           phong=phong,
                           loaiphong=loaiphong,
                           pages = math.ceil(couter/app.config['PAGE_SIZE']))


@app.route("/phong/<int:phong_id>")
def phong_detail(phong_id):
    phong = dao.get_phong_by_id(phong_id)

    return render_template('phong_detail.html', p=phong)


@annonymous_user
def login_my_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            url_next = request.args.get('next')

            return redirect(url_next if url_next else '/')

    return render_template('login.html')

@app.route('/login-admin',methods=['post'])
def login_admin():
    username=request.form['username']
    password=request.form['password']

    user= dao.auth_user(username=username,password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')
@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

if __name__ == '__main__':
    app.run(debug=True)
