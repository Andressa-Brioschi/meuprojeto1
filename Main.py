from flask  import Flask, render_template, request, redirect, flash, url_for
#permissão: pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# biblioteca responsável pelo gerenciamneto do login (precisa do pip install flask-login ) 
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user

# a linha abaixo inicia a variavel de aplicação
#Se não colocar URI não tem como conectar o banco em pg html
app = Flask(__name__)

#permite o flask_login funcionar corretamente 
app.secret_key="MedDay"

#Variável que permite o acesso ao flask_login atravéz da variável de aplicação utilizada como parâmetro 
lm = LoginManager(app)

#faz com que caso o usuário não esteja logado seja direcionado autoamticamente para login
lm.login_view = '/login'

app.config['SQLALCHEMY_DATABASE_URI']  = \
    'mysql+pymysql://root:Lucas_62@localhost:3306/projeto_semestral'

#a linha abaixo instancia o banco de dados
db = SQLAlchemy(app)


#UserMixin permite que o flask_login reconhecer a seguinte classe de usuário
class Cadastro_paciente(UserMixin, db.Model):
    nome = db.Column(db.String(200), nullable = False)
    cpf = db.Column(db.String(11), primary_key =True)
    email = db.Column(db.String(200),  nullable=False)
    data_nasc = db.Column(db.String(200),  nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(11), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    rua = db.Column(db.String(200), nullable=True)
    bairro = db.Column(db.String(200), nullable=True)
    cidade = db.Column(db.String(200), nullable=True)
    UF = db.Column(db.String(2), nullable=False)

    #O UserMixin por padrão espera que exista um campo chamado id para usar como identificador,
    #mas já que cpf é o indentificador é necessáio usar a seguinte função para mudar o identificador padrão 
    def get_id(self):
        return str(self.cpf)

#variável que carrega o usuário atravez da sua busca do seu cpf
@lm.user_loader
def user_loader(cpf):
    usuario = db.session.query(Cadastro_paciente).filter_by(cpf = cpf).first()
    return usuario

@app.route("/cadastrar")
def cadastrar_usuario():
    return render_template("./cadastrar.html")

@app.route("/resetar")
def resetar_senha():
    return  render_template("./resetarsenha.html")

@app.route("/")
#faz com que essa rota só possa ser acessada se estiver logado
@login_required
def home():
    return render_template("./home.html", nome = current_user.nome, email = current_user.email)

@app.route('/logout')
@login_required
def logout():
    #realiza o logout do usuário
    logout_user()
    return redirect(url_for('home'))

@app.route("/add", methods = ['POST'])
def add_banco():
    nome_input = request.form['nome']
    cpf_input = request.form['cpf']
    email_input = request.form['email']
    data_input = request.form['datanasc']
    tel_input = request.form['telefone']
    senha_input = request.form['senha']
    validsenha_input = request.form['validsenha']
    cep_input = request.form['cep']
    rua_input = request.form['rua']
    bairro_input = request.form['bairro']
    cidade_input = request.form['cidade']
    estado_input = request.form['UF']
        
    novo_usuario = Cadastro_paciente(nome = nome_input, cpf = cpf_input, data_nasc = data_input,
            email = email_input, senha = senha_input, telefone = tel_input, cep = cep_input, rua =  rua_input,
            bairro = bairro_input, cidade = cidade_input, UF = estado_input)


    #a  linha abaixo é equivalente a um select no banco, onde na clausula where vai o cpf imputado
    user = db.session.query(Cadastro_paciente).filter_by(cpf = cpf_input ).first()
    if user:
        alert = True

        alert_txt = "Esse CPF já foi cadastrado"

        return render_template("./cadastrar.html", alert_value = alert)

    else:
        if senha_input != validsenha_input:
            alert = True
            alert_txt = "As senhas não coincidem"
        else:    
            alert = False
            alert_txt = ""
            #a linha abaixo adiciona os dados para verificação da entrada de dados
            db.session.add(novo_usuario)


            #a linha abaixo grava as alterações no banco de dados
            db.session.commit()

    return render_template("./cadastrar.html", alert_value = alert, txt_alert = alert_txt)
    #a linha abaixo grava as alterações no banco de dados
    #db.session.commit()
    #return redirect ("/login")
    
    


@app.route("/reset_password", methods = ['POST'])
def reset_password():

    cpf_input = request.form['cpf']
    user = db.session.query(Cadastro_paciente).filter_by(cpf = cpf_input ).first()

    if user:
        alert = False
        old = request.form['senha_antiga']
        old_senha = db.session.query(Cadastro_paciente).filter_by(cpf = cpf_input, senha = old).first()
        if old_senha:
            new = request.form['senha_nova']
            if new == old:
                alert = True
                alert_txt = 'Sua sennha nova não pode ser igual a atual' 
            else:
                alert_txt = '' 
                user.senha = new
                #a linha abaixo grava as alterações no banco de dados
                db.session.commit()          
        else:
            alert = True
            alert_txt = 'Senha antiga inválida'     
    else:
        alert = True
        alert_txt = 'CPF não válido' 
    return render_template("./resetarsenha.html",alert_value = alert, txt_alert = alert_txt)

@app.route("/login", methods = ['GET','POST'])
def logar():
    #se o método da requisição for GET: 
    if request.method == 'GET':
        return render_template('./login.html')
    #se o método da requisição for POST: 
    elif request.method == 'POST':
        email_input = request.form['email']
        senha_input = request.form['senha']
        user = db.session.query(Cadastro_paciente).filter_by(email = email_input, senha = senha_input).first()
        if not user:
            return "Email ou senha incorretos."
        else:
            #realiza o login do usuário
            login_user(user)
            #redireciona para home depois do login
            return redirect(url_for('home')) 

app.run(debug=True)