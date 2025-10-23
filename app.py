from flask import Flask
from models import db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '4b613365e58aed8a91ecf761164c249f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///receitas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)