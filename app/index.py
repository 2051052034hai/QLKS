from flask import Flask, render_template, request
from app import app, dao


@app.route("/")
def index():
    ma_lp = request.args.get('maLoaiPhong')
    kw = request.args.get('Keyword')
    phong = dao.load_Phong(ma_lp=ma_lp, kw=kw)
    return render_template('index.html', phong=phong)


if __name__ == '__main__':
    app.run(debug=True)
