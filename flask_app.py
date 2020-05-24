from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone

app = Flask(__name__)

# configurar o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BancoProvaFinal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# criar o modelo para o registro do usuario
class Apontamento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_usuario = db.Column(db.String(25), nullable=True)
    #hora = db.Column(db.DateTime, default=datetime.now)
    hora = db.Column(db.DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))

    @property
    def serializar(self):
        return {
            'id': self.id,
            'nome_usuario': self.nome_usuario,
            'hora': str(self.hora)[11:16]
        }


class Contato(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String(10), nullable=True)
    sobrenome = db.Column(db.String(25), nullable=True)
    email = db.Column(db.String(35), nullable=True)
    assunto = db.Column(db.String(15), nullable=True)
    hora = db.Column(db.DateTime, default=datetime.now)
    mensagem = db.Column(db.String(150),nullable=True)

db.create_all()

@app.route('/inicio')
@app.route('/')
def inicio():
    return render_template('index.html')



@app.route('/funcionarios', methods=['GET', 'POST'])
def funcionarios():
    if request.method == "POST":
        print(request.form['nome'])
        usuario = Apontamento(nome_usuario=request.form['nome'])
        db.session.add(usuario)
        db.session.commit()
        return render_template('index.html')

    if request.method == "GET":
        ultimos10 = Apontamento.query.order_by(-Apontamento.id).limit(10).all()
        print(ultimos10)
        return jsonify(funcionarios=[i.serializar for i in ultimos10])



@app.route('/contato')
def contato():
    return render_template('contato.html')



@app.route('/seus_dados', methods=['GET','POST'])
def seus_dados():
    if request.method == 'POST':
        print(request.form['nome'])

        usuario = Contato(nome=request.form['nome'], sobrenome=request.form['sobrenome'], 
                          email=request.form['email'], assunto=request.form['assunto'], 
                          mensagem=request.form['mensagem'])
        db.session.add(usuario)
        db.session.commit()

        return  render_template('obrigado.html')



@app.route('/obrigado')
def obrigado():
    return render_template('obrigado.html')
    

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/curso')
def curso():
    return render_template('curso.html')

## Para rodar o projeto em desenvolvimento

if __name__ == '__main__':
    app.run(debug=True)
