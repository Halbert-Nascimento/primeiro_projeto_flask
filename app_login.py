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
    return redirect(url_for('pagina_inicial'))

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




if __name__ == '__main__':
    app.run(debug=True)