from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = '2324qwe233@#@wc3qf3qfe3fefe*&@WY&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:8643947@localhost/hoteldb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 3
db = SQLAlchemy(app=app)
login = LoginManager(app=app)
cloudinary.config(
    cloud_name='dcteoaxmv',
    api_key='216696992118656',
    api_secret='ex3r-7to2iHTnf3rqvFNHjYr1ng'
)
