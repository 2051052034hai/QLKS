from flask import Flask, render_template, request,redirect
from app import app, dao
from flask_login import login_user, logout_user, login_required
from app.decorators import annonymous_user
from app.admin import *
@app.route("/")
def index():
    ma_lp = request.args.get('maLoaiPhong')
    kw = request.args.get('Keyword')
    phong = dao.load_Phong(ma_lp=ma_lp, kw=kw)
    loaiphong = dao.load_LoaiPhong()
    return render_template('index.html', phong=phong, loaiphong = loaiphong)

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


if __name__ == '__main__':

    app.run(debug=True)
