from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#configuração do aplicativo e banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://halbert:0987654321@localhost/flask_db'
app.config['SECRET_KEY'] = 'halbert@@123'
db = SQLAlchemy(app)

#configurando flask login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Usuario(UserMixin, db.Model):
  __tablename__ = 'usuarios'
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  senha = db.Column(db.String(100), nullable=False)

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
    return redirect(url_for('login'))

# Rota protegida que requer autenticação
@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', usuario=current_user)

@app.route('/usuario')
def usuario():
    return render_template('usuario.html')

####
#aqui pagina inicial
###
@app.route('/')
def pagina_inicial():
    return render_template('index.html', mensagem="Bem vindo a pagina inicial!")



@app.route('/usuarios')
def usuarios():
    # Conectando ao banco de dados
    cur = mysql.connection.cursor()
    # Executa uma query, solicitação ao DB
    # onde seleciona/busca/retonar todos'*'  registo da tabela usuarios
    cur.execute('SELECT * FROM usuarios')    
    # Obtém os resultados fetchall
    resultados = cur.fetchall()
    # Fecha a conexão
    cur.close()
    # Renderiza o template 'usuarios.html' com os resultados
    return render_template('usuarios.html', resultados=resultados)

"""
methods=['GET', 'POST'] especifica que essa rota aceita tanto requisições GET quanto POST.Essa rota é acessível quando você acessa a URL via navegador (GET) e quando envia um formulário (POST).
"""
@app.route('/adicionar_usuario', methods=['GET', 'POST'])
def adicionar_usuario():
    #se for uma requisição de envio de formulario
    if request.method == 'POST':
        detalhes_usuario = request.form
        nome = detalhes_usuario['nome']
        email = detalhes_usuario['email']
        senha = detalhes_usuario['senha']

        # Lógica para salvar imagens (enviadas via formulário)
        imagens = request.files.getlist("imagem")
        
        caminhos_imagens = []

        for imagem in imagens:
            # Define o caminho onde a imagem será salva
            caminho_imagen = f"static/imagens/{imagem.filename}"
            #para cada imagem Define o caminho onde a imagem será salva e add a lista
            caminhos_imagens.append(caminho_imagen)
            # Salva a imagem no caminho especificado
            imagem.save(caminho_imagen)

        # Conecta ao banco de dados
        cur = mysql.connection.cursor()
        # Executa a query para inserir o usuário no banco de dados
        cur.execute("INSERT INTO usuarios(nome, email, senha, imagem1, imagem2,imagem3) VALUES (%s,%s,%s,%s,%s,%s)", (nome, email, senha,caminhos_imagens[0],caminhos_imagens[1],caminhos_imagens[2]))

         # Comita/salva as alterações
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('usuarios'))
    
    #se for uma requisição de acesso via URL navegador (GET)
    return render_template('adicionar_usuario.html')

"""
Atualizando Dados do Usuário:
adicionar a capacidade de atualizar os dados do usuário no banco de dados. 
"""
#quando chama o link ja e passado a id do usuario dentrodo link:( link/<int:id>)
@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    # Conecta ao banco de dados
    cur = mysql.connection.cursor()
    #Seleciona e recupere todas as colunas da tabela usuarios com a id específica.
    cur.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
    # Obtém um único registro (o usuário com o ID fornecido)
    usuario = cur.fetchone()
    cur.close()

    #verifica se e uma solicitação POST
    if request.method == 'POST':
        #obtem os dados do usuario do formulario
        detalhes_usuario = request.form
        nome = detalhes_usuario['nome']
        email = detalhes_usuario['email']
        senha = detalhes_usuario['senha']

        #logica salvar img
        imagens = request.files.getlist("imagem")
        caminhos_imagens = []

        for imagem in imagens:
            caminho_imagem = f"static/imagens/{imagem.filename}"
            caminhos_imagens.append(caminho_imagem)
            imagem.save(caminho_imagem)

        #conecta novamnete ao DB
        cur = mysql.connection.cursor()

        # Executa a query para atualizar os dados do usuário com o ID fornecido
        #quando e update usa UPDATE usuarios SET nome=%s, (nome, id))
        #quando e insert usar usuarios(nome) VALUES (%s)
        cur.execute("UPDATE usuarios SET nome=%s, email=%s, senha=%s, imagem1=%s, imagem2=%s, imagem3=%s WHERE id=%s", (nome, email, senha, caminhos_imagens[0], caminhos_imagens[1], caminhos_imagens[2], id))

        #commit salva as informações no DB
        mysql.connection.commit()
        cur.close()

        # Redireciona para a página de usuários após a edição bem-sucedida se methodo for post
        return redirect(url_for('usuarios'))
    # Renderiza o formulário preenchido com os dados atuais do usuário se method for get
    return render_template('editar_usuario.html', usuario=usuario)

"""
Exclusão de Usuário:
Vamos adicionar a capacidade de excluir um usuário do banco de dados.
"""
@app.route('/excluir_usuario/<int:id>', methods=['GET', 'POST'])
def excluir_usuario(id):
    cur = mysql.connect.cursor()

    if request.method == 'POST':
        # Executa a query para excluir o usuário com o ID fornecido
        """
        Segunda consulta e verificado se a solicitação é do tipo POST, Se for, a segunda consulta é executada para excluir o usuário com o ID fornecido.
        """
        cur.execute("DELETE FROM usuarios WHERE id=%s",(id,))

        mysql.connection.commit()
        cur.close()

        #redireciona para pagine de usuarios apos exclusão
        return redirect(url_for('usuarios'))
    
    # Executa a query para obter as informações do usuário com o ID fornecido
    """
    Primeira consulta é utilizada para obter as informações do usuário com o ID fornecido. O resultado dessa consulta é armazenado na variável usuario com o fetchone()
    """
    cur.execute('SELECT * FROM usuarios WHERE id=%s',(id,))
    usuario = cur.fetchone()

    cur.close()
    """
    A primeira consulta é realizada para obter informações sobre o usuário que será excluído, e a segunda consulta é executada apenas se a confirmação da exclusão for recebida por meio de uma solicitação POST. 
    """

    return render_template('excluir_usuario.html', usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)