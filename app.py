from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Receita
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = '4b613365e58aed8a91ecf761164c249f'

database_url = os.environ.get('DATABASE_URL', 'sqlite:///receitas.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Pasta onde as imagens serão salvas
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Limite de 5MB por imagem
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}  # Tipos permitidos
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db.init_app(app)

# Criar tabelas
with app.app_context():
    db.create_all()
    try:
        from sqlalchemy import text
        db.session.execute(text("""
            ALTER TABLE receita 
            ADD COLUMN IF NOT EXISTS imagem VARCHAR(300);
        """))
        db.session.commit()
        print("✅ Coluna 'imagem' verificada/criada!")
    except Exception as e:
        print(f"ℹ️ Coluna já existe ou erro: {e}")
        db.session.rollback()

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
            flash('Este email já está cadastrado!')
            return redirect(url_for('cadastro'))
        
        # VALIDAÇÃO DE SENHA FORTE
        if len(senha) < 8:
            flash('A senha deve ter no mínimo 8 caracteres!')
            return redirect(url_for('cadastro'))
        
        if not any(c.isupper() for c in senha):
            flash('A senha deve conter pelo menos uma letra MAIÚSCULA!')
            return redirect(url_for('cadastro'))
        
        if not any(c.islower() for c in senha):
            flash('A senha deve conter pelo menos uma letra minúscula!')
            return redirect(url_for('cadastro'))
        
        if not any(c.isdigit() for c in senha):
            flash('A senha deve conter pelo menos um número!')
            return redirect(url_for('cadastro'))
        
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in senha):
            flash('A senha deve conter pelo menos um caractere especial (!@#$%^&*)')
            return redirect(url_for('cadastro'))
        
        # Cria novo usuário
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login.')
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

# Rota de perfil
@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        acao = request.form.get('acao')
        
        # ATUALIZAR INFORMAÇÕES BÁSICAS (nome e email)
        if acao == 'atualizar_info':
            novo_nome = request.form.get('nome')
            novo_email = request.form.get('email')
            
            # Validar se campos não estão vazios
            if not novo_nome or not novo_email:
                flash('Nome e email são obrigatórios!')
                return redirect(url_for('perfil'))
            
            # Verificar se email já existe (se mudou)
            if novo_email != current_user.email:
                email_existe = Usuario.query.filter_by(email=novo_email).first()
                if email_existe:
                    flash('Este email já está em uso!')
                    return redirect(url_for('perfil'))
            
            # Atualizar dados
            current_user.nome = novo_nome
            current_user.email = novo_email
            db.session.commit()
            
            flash('Informações atualizadas com sucesso!')
            return redirect(url_for('perfil'))
        
        # ALTERAR SENHA
        elif acao == 'alterar_senha':
            senha_atual = request.form.get('senha_atual')
            nova_senha = request.form.get('nova_senha')
            confirmar_senha = request.form.get('confirmar_senha')
            
            # Verificar se a senha atual está correta
            if not check_password_hash(current_user.senha, senha_atual):
                flash('Senha atual incorreta!')
                return redirect(url_for('perfil'))
            
            # Validar nova senha
            if nova_senha != confirmar_senha:
                flash('As senhas não coincidem!')
                return redirect(url_for('perfil'))
            
            # VALIDAÇÃO DE SENHA FORTE
            if len(nova_senha) < 8:
                flash('A senha deve ter no mínimo 8 caracteres!')
                return redirect(url_for('perfil'))
            
            if not any(c.isupper() for c in nova_senha):
                flash('A senha deve conter pelo menos uma letra MAIÚSCULA!')
                return redirect(url_for('perfil'))
            
            if not any(c.islower() for c in nova_senha):
                flash('A senha deve conter pelo menos uma letra minúscula!')
                return redirect(url_for('perfil'))
            
            if not any(c.isdigit() for c in nova_senha):
                flash('A senha deve conter pelo menos um número!')
                return redirect(url_for('perfil'))
            
            if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in nova_senha):
                flash('A senha deve conter pelo menos um caractere especial (!@#$%^&*)')
                return redirect(url_for('perfil'))
            
            # Atualizar senha
            current_user.senha = generate_password_hash(nova_senha)
            db.session.commit()
            
            flash('Senha alterada com sucesso!')
            return redirect(url_for('perfil'))
    
    return render_template('perfil.html')

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

        imagem_path = None
        if 'imagem' in request.files:
            file = request.files['imagem']
            # Se o usuário selecionou um arquivo válido
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                imagem_path = f"uploads/{filename}"
        
        nova_receita = Receita(
            nome=nome,
            ingredientes=ingredientes,
            modo_preparo=modo_preparo,
            tempo_preparo=tempo_preparo,
            categoria=categoria,
            dificuldade=dificuldade,
            imagem=imagem_path,
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
        
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file and file.filename != '' and allowed_file(file.filename):
                # Deletar imagem antiga se existir
                if receita.imagem:
                    old_image_path = os.path.join('static', receita.imagem)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                # Salvar nova imagem
                filename = secure_filename(file.filename)
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                receita.imagem = f"uploads/{filename}"
        
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