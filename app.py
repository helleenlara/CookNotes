from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Receita
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '4b613365e58aed8a91ecf761164c249f'

database_url = os.environ.get('DATABASE_URL', 'sqlite:///receitas.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Criar tabelas
with app.app_context():
    db.create_all()

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
        
        usuario_existe = Usuario.query.filter_by(email=email).first()
        if usuario_existe:
            flash('Email já cadastrado!')
            return redirect(url_for('cadastro'))
        
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

# Rota principal
@app.route('/')
@login_required
def index():
    query = Receita.query.filter_by(usuario_id=current_user.id)
    busca = request.args.get('busca')
    if busca:
        query = query.filter(Receita.nome.contains(busca))
    categoria = request.args.get('categoria')
    if categoria:
        query = query.filter_by(categoria=categoria)
    receitas = query.all()
    return render_template('index.html', receitas=receitas)

# Rota adicionar receita
@app.route('/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_receita():
    if request.method == 'POST':
        nome = request.form['nome']
        ingredientes = request.form['ingredientes']
        modo_preparo = request.form['modo_preparo']
        tempo_preparo = request.form['tempo_preparo']
        categoria = request.form['categoria']
        dificuldade = request.form['dificuldade']
        
        nova_receita = Receita(
            nome=nome,
            ingredientes=ingredientes,
            modo_preparo=modo_preparo,
            tempo_preparo=tempo_preparo,
            categoria=categoria,
            dificuldade=dificuldade,
            usuario_id=current_user.id
        )
        db.session.add(nova_receita)
        db.session.commit()
        flash('Receita adicionada com sucesso!')
        return redirect(url_for('index'))
    return render_template('adicionar_receita.html')

# Rota para visualizar receita
@app.route('/receita/<int:id>')
@login_required
def visualizar_receita(id):
    receita = Receita.query.get_or_404(id)
    if receita.usuario_id != current_user.id:
        flash('Você não tem permissão para ver esta receita!')
        return redirect(url_for('index'))
    return render_template('visualizar_receita.html', receita=receita)

#Rota editar receita
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_receita(id):
    receita = Receita.query.get_or_404(id)
    if receita.usuario_id != current_user.id:
        flash('Você não tem permissão para editar esta receita!')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        receita.nome = request.form['nome']
        receita.ingredientes = request.form['ingredientes']
        receita.modo_preparo = request.form['modo_preparo']
        receita.tempo_preparo = request.form['tempo_preparo']
        receita.categoria = request.form['categoria']
        receita.dificuldade = request.form['dificuldade']
        
        db.session.commit()
        flash('Receita atualizada com sucesso!')
        return redirect(url_for('visualizar_receita', id=receita.id))
    
    return render_template('editar_receita.html', receita=receita)

# Rota para deletar receita
@app.route('/deletar/<int:id>')
@login_required
def deletar_receita(id):
    receita = Receita.query.get_or_404(id)
    if receita.usuario_id != current_user.id:
        flash('Você não tem permissão para deletar esta receita!')
        return redirect(url_for('index'))
    
    db.session.delete(receita)
    db.session.commit()
    flash('Receita deletada com sucesso!')
    return redirect(url_for('index'))

#Debug listar todas as rotas
print("\n" + "="*50)
print("🔍 ROTAS REGISTRADAS NO FLASK:")
print("="*50)
for rule in app.url_map.iter_rules():
    print(f"  {rule.endpoint:30s} -> {rule.rule}")
print("="*50 + "\n")

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)