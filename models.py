from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    receitas = db.relationship('Receita', backref='autor', lazy=True)

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    ingredientes = db.Column(db.Text, nullable=False)
    modo_preparo = db.Column(db.Text, nullable=False)
    tempo_preparo = db.Column(db.Integer)  # em minutos
    categoria = db.Column(db.String(50))
    dificuldade = db.Column(db.String(20))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)