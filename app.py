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

# Definição da classe 'Usuario' para representar usuários no banco de dados.
class Usuario(UserMixin, db.Model):
  __tablename__ = 'usuarios' # especifica o nome correto da tabela queesta no DB
  id = db.Column(db.Integer, primary_key=True) # Campo de chave primária
  nome = db.Column(db.String(100), nullable=False) # Nome do usuário (obrigatório)
  email = db.Column(db.String(100), unique=True, nullable=False)  # Email do usuário (único e obrigatório)
  senha = db.Column(db.String(100), nullable=False) # Senha do usuário (obrigatória)
  telefone = db.Column(db.String(20)) # Número de telefone do usuário
  imagem_perfil = db.Column(db.String(255))  # Caminho da imagem de perfil
# Relacionamento de usuario e produto
  produtos=db.relationship('Produto', back_populates='usuario')

# Definição da classe 'Produto' para representar produtos no banco de dados.
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Campo de chave primária
    nome_produto = db.Column(db.String(255), nullable=False) # Nome do produto (obrigatório)
    tipo_produto = db.Column(db.String(255)) # Tipo do produto
    descricao_produto = db.Column(db.Text) # Descrição do produto
    imagem1=db.Column(db.String(255))  # Caminho das imagens 1 a 3
    imagem2=db.Column(db.String(255))
    imagem3=db.Column(db.String(255))

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False) # Chave estrangeira para relacionar o produto ao usuário
    usuario = db.relationship('Usuario', back_populates='produtos') # Relacionamento com a classe 'Usuario' indicando o proprietário do produto


#callback para carregar o usuario a partir da ID
# Esta função load_user é usada pelo Flask-Login para carregar um objeto de usuário a partir do ID fornecido durante a sessão do usuário
@login_manager.user_loader
def load_user(user_id):
  # consulta o banco de dados para obter o objeto de usuário correspondente ao ID fornecido.
  return Usuario.query.get(int(user_id))
  

#Adicionar Rotas de Autenticação
#adicionando rotas para lidar com o login, logout e proteção de rotas autenticadas
# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    mensagem=""
    if current_user.is_authenticated:
        # se tiver logado redireciona para pagina de perfil
        return redirect(url_for('perfil'))
    else: # se não tiver logado receb os dados do formulario de login
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            usuario = Usuario.query.filter_by(email=email).first() #fax pesquisa no DB pelo email para saber se esta cadastrado 

            if usuario and usuario.senha == senha: #confirma se a senha esta correta
                login_user(usuario)
                
                return redirect(url_for('perfil'))
            else: # se a senha tiver errada ou usuario não cadastrado informa mensagem de erro
                mensagem = "Credenciais invalidas!"

        return render_template('login.html', mensagem=mensagem)

# Rota de logout
@app.route('/logout')
@login_required # necessrio estar logado para executar essa função
def logout():
    logout_user()
    print("deslogado") # printa mensagem deslogado para debug
    return redirect(url_for('pagina_inicial')) # redireciona para pagina inicial apos logout

# Rota cadastrar usuario, aceita solicitações get e post
@app.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST': # se solicitação for tipo post pega requerimento de formulario
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        telefone = request.form['telefone']
        # imagem_perfil = request.form['imagem_perfil']

        #criando uma instacia do modelo Usuario
        novo_usuario = Usuario(nome=nome, email=email, senha=senha, telefone =telefone )

        
        db.session.add(novo_usuario) # adicionando novo usuario ao DB
        db.session.commit() # salva as informações no Db

        print("Usuario cadastrado com sucesso") #mensagem pra debug
        return redirect(url_for('login')) # redireciona para pagina de login apos cadastro
    return render_template('cadastrar_usuario.html') # renderiza a pagina cadastro usuario se a solicitação for get

# Rota de perfil 
@app.route('/perfil')
@login_required # para acessar rota de perfil e necessario estar logdo
def perfil():
    total_produtos =Produto.query.filter_by(id_usuario=current_user.id).count() # query de quantos itens esse usuario tem cadastrado
    return render_template('perfil.html', usuario=current_user, total_produtos=total_produtos) # renderiza a pagina com as informações de usuario e td de itens passadas,

# função para verificar se esta logado
def usuariologado(current_user):
    #verifica se ta logado e retonar o nome
    if current_user.is_authenticated:
        nome_usuario = f"{current_user.nome}"
    else:
        nome_usuario = ""
    return nome_usuario

####
#aqui pagina inicial
###

# rota d pagina inicial index.html
@app.route('/')
def pagina_inicial():
    produtos = Produto.query.join(Produto.usuario).all() # query d todos os produtos no DB
    return render_template('index.html', mensagem="Bem vindo a pagina inicial!", nome_usuario=usuariologado(current_user), produtos=produtos)
    # renderiza a pagina com as informações de usuario e mensagem passadas,

# Rota de cadastro produtos, aceita solicitações get e post
@app.route('/cadastrar_produto', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    if request.method== 'POST': # se solicitação for tipo post pega requerimento de formulario
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
       
               

        #criando instacia modelo Produtos
        novo_produto = Produto(
            nome_produto=nome_produto,
            tipo_produto=tipo_produto,
            descricao_produto=descricao_produto,
            imagem1=caminho_imagem1,
            imagem2=caminho_imagem2,
            imagem3=caminho_imagem3,
            usuario=current_user #relacionar o produto ao usuario logado
        )

        #adc o novo produto ao Db
        db.session.add(novo_produto)
        db.session.commit() # salva as alerações

        flash('Produttos cadasrado com sucesso!', 'succes') #passa mensagem direto para o html 
        return redirect(url_for('perfil')) # apos cadastrar item edireciona para pag perfil
    usuario=current_user    
    return render_template('cadastrar_produto.html', usuario=usuario)

#Rota para listar produtos do usuario logado
@app.route('/listar_produtos')
@login_required # necessrio estar logado
def listar_produtos():
    # busca produtos do usuario logado no momento
    produtos =Produto.query.filter_by(id_usuario=current_user.id).all()
    # produtos =Produto.query.filter_by(id_usuario=current_user.id).limit(6).all()
    
    return render_template('listar_produtos.html', usuario=current_user, produtos=produtos)

#rota para exlusão de produtos cadastrados
@app.route('/excluir_item/<int:id>', methods=['GET', 'POST'])
@login_required
def excluir_item(id):
    #retonar o produto, se não achar retonar um erro 404 pag
    produto = Produto.query.get_or_404(id)

    #verifica se o produto realmente corresponde ao usuario
    if produto.usuario == current_user:   
        db.session.delete(produto)
        db.session.commit()        
    else:
        #'se não' gera mensagem de erro
        print("erro(403)")

    return redirect(url_for('listar_produtos'))


@app.route('/buscar_produtos', methods=['GET'])
def buscar_produtos():
    #obte parametros
    nome_produto = request.args.get('nome_produto', '')
    tipo_produto = request.args.get('tipo_produto', '')

    #buscando no bando de dados
    produtos = Produto.query.filter(
        Produto.nome_produto.ilike(f"%{nome_produto}"),
        Produto.tipo_produto.ilike(f"%{tipo_produto}")
    ).all()
    """
    A função ilike é usada para realizar uma pesquisa de substring insensível a maiúsculas e minúsculas no banco de dados.
    """

    # return render_template('listar_produtos.html',usuario=current_user, produtos=produtos)
    return render_template('index.html', nome_usuario=usuariologado(current_user), produtos=produtos)



# Executa o aplicativo Flask apenas se este script estiver sendo executado diretamente.
if __name__ == '__main__':
    app.run(debug=True)