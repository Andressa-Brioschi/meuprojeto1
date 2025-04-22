from flask  import Flask, render_template, request, redirect, flash, url_for, session
#permissão: pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# a linha abaixo inicia a variavel de aplicação
#Se não colocar URI não tem como conectar o banco em pg html
app = Flask(__name__)

#permite o flask_login funcionar corretamente 
app.secret_key="SenhaSuperSecreta"


app.config['SQLALCHEMY_DATABASE_URI']  = \
    'mysql+pymysql://root:we123@localhost:3306/projeto_semestral'

#a linha abaixo instancia o banco de dados
db = SQLAlchemy(app)


# session['nomeDaSessao'] = request.form['cpf']

class Cadastro_paciente(db.Model):
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

@app.route("/login")
def telaInicial():
    return render_template("./login.html")

@app.route("/cadastrar")
def cadastrar_usuario():
    return render_template("./cadastrar.html")

@app.route("/resetar")
def resetar_senha():
    return  render_template("./resetarsenha.html")


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
            return redirect ("/login")

 
    
@app.route ("/autenticar", methods = ['POST'])
def autenticar():    
    cpf = request.form['txtcpf']
    senha = request.form['txtsenha']
    #a  linha abaixo é equivalente a um select no banco, onde na clausula where vai o cpf imputado e a senha
    user = db.session.query(Cadastro_paciente).filter_by(cpf = cpf, senha = senha ).first()

    if user:
        return render_template("./home.html")
    else:
        return render_template("./login.html")

        
    



    


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


app.run(debug=True)