from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Receita
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '4b613365e58aed8a91ecf761164c249f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///receitas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rota de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        # Verifica se email já existe
        usuario_existe = Usuario.query.filter_by(email=email).first()
        if usuario_existe:
            flash('Email já cadastrado!')
            return redirect(url_for('cadastro'))
        
        # Cria novo usuário
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos!')
    
    return render_template('login.html')

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rota principal (temporária)
@app.route('/')
@login_required
def index():
    return '<h1>Bem-vindo ao CookNotes!</h1><a href="/logout">Sair</a>'

# Criar as tabelas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)