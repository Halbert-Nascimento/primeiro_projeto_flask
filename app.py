from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
from flask_migrate import Migrate


#configuração do aplicativo e banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://halbert:0987654321@localhost/flask_db'
app.config['SECRET_KEY'] = 'halbert@@123'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#configurando flask login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Usuario(UserMixin, db.Model):
  __tablename__ = 'usuarios'
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  senha = db.Column(db.String(100), nullable=False)
  telefone = db.Column(db.String(20))
# Relacionamento um-para-muitos (um usuário pode ter vários produtos)
  produtos=db.relationship('Produto', back_populates='usuario')

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String(255), nullable=False)
    tipo_produto = db.Column(db.String(255))
    descricao_produto = db.Column(db.Text)
    imagem1=db.Column(db.String(255))
    imagem2=db.Column(db.String(255))
    imagem3=db.Column(db.String(255))

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', back_populates='produtos')




#callback para carregar o usuario a partir da ID
@login_manager.user_loader
def load_user(user_id):
  return Usuario.query.get(int(user_id))
  

#Adicionar Rotas de Autenticação
#adicionando rotas para lidar com o login, logout e proteção de rotas autenticadas
# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.senha == senha:
            login_user(usuario)
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('perfil'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')

    return render_template('login.html')

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout bem-sucedido!', 'success')
    print("deslogado")
    return redirect(url_for('pagina_inicial'))

#cadastrar usuario
@app.route('/cadastrar_usuario', methods=['GET', 'POST'])
# @login_required
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        telefone = request.form['telefone']

        #criando uma instacia do modelo Usuario
        novo_usuario = Usuario(nome=nome, email=email, senha=senha, telefone =telefone )

        #adicionando novo usuario ao DB
        db.session.add(novo_usuario)
        db.session.commit()

        print("Usuario cadastrado com sucesso")
        return redirect(url_for('login'))
    return render_template('cadastrar_usuario.html')

# Rota protegida que requer autenticação
@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', usuario=current_user, produto=Produto)

####
#aqui pagina inicial
###
@app.route('/')
def pagina_inicial():
    #verifica se ta logado para colocaro nome de user ou registrar
    if current_user.is_authenticated:
        registrar = f"{current_user.nome}"
    else:
        registrar = f"Registrar"

    produtos = Produto.query.all()
    return render_template('index.html', mensagem="Bem vindo a pagina inicial!", registrar=registrar, produtos=produtos)

@app.route('/cadastrar_produto', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    if request.method== 'POST':
        nome_produto = request.form['nome_produto']
        tipo_produto = request.form['tipo_produto']
        descricao_produto = request.form['descricao_produto']

        imagem1 = request.files.get('imagem1')
        imagem2 = request.files.get('imagem2')
        imagem3 = request.files.get('imagem3')
        
        caminho_imagem1 = f"static/imagens/{imagem1.filename}"
        imagem1.save(caminho_imagem1)
        caminho_imagem2 = f"static/imagens/{imagem2.filename}"
        imagem2.save(caminho_imagem2)
        caminho_imagem3 = f"static/imagens/{imagem3.filename}"
        imagem3.save(caminho_imagem3)
       
        caminho_imagem1 = f"static/imagens/{imagem1.filename}"
        caminho_imagem2 = f"static/imagens/{imagem2.filename}"
        caminho_imagem2 = f"static/imagens/{imagem3.filename}"

        

        #criando instacia modelo Produtos
        novo_produto = Produto(
            nome_produto=nome_produto,
            tipo_produto=tipo_produto,
            descricao_produto=descricao_produto,
            imagem1=caminho_imagem1,
            imagem2=caminho_imagem2,
            imagem3=caminho_imagem2,
            usuario=current_user #relacionar o produto ao usuario logado
        )

        #adc o novo produto ao Db
        db.session.add(novo_produto)
        db.session.commit()

        flash('Produttos cadasrado com sucesso!', 'succes')
        return redirect(url_for('perfil'))
    usuario=current_user    
    return render_template('cadastrar_produto.html', usuario=usuario)


@app.route('/produtos')
def listar_produtos():
    # produtos = Produto.query.all() busca todos os produtos
    produtos =Produto.query.filter_by(id_usuario=current_user.id).limit(6).all()
    
    return render_template('listar_produtos.html', usuario=current_user, produtos=produtos)


if __name__ == '__main__':
    app.run(debug=True)