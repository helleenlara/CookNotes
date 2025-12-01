# CookNotes  
Gerenciador de Receitas – Aplicação Web desenvolvida para a disciplina **Desenvolvimento Web Python – Paradigmas**.

**Autora:** Lara Hellen Marques  
**Deploy:** https://cooknotes-production.up.railway.app/login
**Apresentação:** https://www.canva.com/design/DAG562BDGGE/cl0bmOru2H1BBlC8uIfLxg/edit?utm_content=DAG562BDGGE&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

---

##  Sobre o projeto

O **CookNotes** é uma aplicação web que permite gerenciar receitas culinárias de forma simples e intuitiva.  
O sistema inclui **autenticação**, **CRUD completo**, **busca**, **perfil do usuário** e está preparado para **deploy em cloud (Railway)**.

Este projeto foi desenvolvido individualmente como parte da Avaliação da disciplina *Desenvolvimento Web Python – Paradigmas*.

---

##  Objetivos acadêmicos atendidos

✔ Implementar uma aplicação web com **frontend (Bootstrap/HTML/CSS/JS)** e **backend em Python**  
✔ Usar um **banco de dados relacional (PostgreSQL)**  
✔ Incluir **login**  
✔ Implementar **mínimo de 2 requisitos funcionais**, e pelo menos **1 com CRUD**  
✔ Publicar em **ambiente cloud (Railway)**  
✔ Entregar **código no GitHub**  
✔ Realizar apresentação em **até 8 min**

---

#  Funcionalidades

###  **1. Login e Autenticação**
- Cadastro de usuário
- Login com verificação
- Armazenamento seguro

###  **2. CRUD de Receitas (RF principal)**
- ✔ Criar receitas  
- ✔ Listar receitas  
- ✔ Editar receitas  
- ✔ Excluir receitas  
- ✔ Visualizar detalhes  

###  **3. Busca e filtros**
- Busca por nome ou categoria

###  **4. Perfil do Usuário**
- Atualizar dados
- Alterar senha com validação forte

---

#  Requisitos Funcionais (RF)

| Código | Descrição |
|-------|-----------|
| **RF01** | Permitir cadastro de usuários |
| **RF02** | Permitir login |
| **RF03** | Criar novas receitas |
| **RF04** | Listar receitas cadastradas |
| **RF05** | Editar receita existente |
| **RF06** | Excluir receita |
| **RF07** | Buscar receitas por termo |
| **RF08** | Permitir editar dados do perfil |

---

#  Requisitos Não Funcionais (RNF)

| Código | Descrição |
|-------|-----------|
| **RNF01** | A senha deve conter letras, números e caracteres especiais |
| **RNF02** | A interface deve ser responsiva (Bootstrap) |
| **RNF03** | O sistema deve rodar em ambiente cloud |
| **RNF04** | Código organizado e versionado via GitHub |
| **RNF05** | Banco de dados deve ser persistente |

---

#  Arquitetura da Aplicação

Usuário
↓
HTML + Bootstrap
↓
Flask (Python)
↓
SQLAlchemy ORM
↓
PostgreSQL (Railway)

---

#  Estrutura de Pastas

CookNotes/
│
├── app.py
├── models.py
├── requirements.txt
├── README.md
│
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── cadastro.html
│ ├── receitas.html
│ ├── criar_receita.html
│ ├── editar_receita.html
│ └── perfil.html
│
└── static/
├── css/
│ └── style.css
├── js/
│ └── script.js
└── img/
└── logo.png


---

#  Modelos (Exemplo)

### **Modelo Usuário**

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

## Modelo Receita

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    ingredientes = db.Column(db.Text, nullable=False)
    modo_preparo = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(50))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

##  Rotas da Aplicação

Rota	Método	Descrição
/	GET	Página inicial
/login	GET/POST	Login
/cadastro	GET/POST	Criar conta
/receitas	GET	Listar receitas
/receitas/criar	GET/POST	Criar receita
/receitas/editar/<id>	GET/POST	Editar receita
/receitas/excluir/<id>	POST	Excluir receita
/perfil	GET/POST	Perfil do usuário

##  Como rodar o projeto localmente

1. Clone o repositório

git clone https://github.com/helleenlara/CookNotes.git
cd CookNotes

2. Crie o ambiente virtual

python -m venv venv

3. Ative o ambiente
Windows
venv\Scripts\activate

Linux/macOS
source venv/bin/activate

4. Instale dependências
pip install -r requirements.txt

5. Configure o arquivo .env

FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_banco
SECRET_KEY=sua_chave_secreta

6. Execute
flask run

##  Deploy no Railway
1.Criar conta no Railway
2.Criar projeto “New Service → Deploy from GitHub”
3.Conectar seu repositório CookNotes
4.Definir variáveis de ambiente conforme .env
5.Conectar PostgreSQL via “Add Plugin”
6.Redeploy automático

##  Licença
Este projeto está sob a licença MIT.

##  Autoria
Desenvolvido por:
Lara Hellen Marques,
Projeto individual – 2025.
