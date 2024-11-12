from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Inicializando o Flask
app = Flask(__name__)

# Configuração do banco de dados (SQLite para desenvolvimento)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Banco de dados local
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'sua-chave-secreta'  # Chave secreta para o JWT

# Inicializar as extensões
db = SQLAlchemy(app)  # Definindo o banco de dados após a criação do app
jwt = JWTManager(app)
CORS(app)  # Habilita CORS para o frontend

# Definindo o modelo do banco de dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Workout {self.name} - {self.duration}>'

# Corrigido: Agora o decorador está depois da definição do app
@app.before_first_request
def create_tables():
    db.create_all()  # Cria todas as tabelas com base nos modelos definidos

# Rota de Login (gera o token JWT)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Verifique as credenciais do usuário aqui (isso pode ser substituído por uma consulta no banco de dados)
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:  # Verificação de senha (use hash de senha para segurança em produção)
        access_token = create_access_token(identity=email)
        return jsonify(token=access_token), 200
    else:
        return jsonify(error="Credenciais inválidas"), 401

# Rota para criar treino (exige autenticação JWT)
@app.route('/api/workouts/create', methods=['POST'])
@jwt_required()
def create_workout():
    current_user = get_jwt_identity()  # Obtém o e-mail do usuário logado
    workout_data = request.get_json()  # Dados do treino enviados pelo frontend

    # Criar e adicionar o treino ao banco de dados
    new_workout = Workout(
        name=workout_data['name'],
        duration=workout_data['duration'],
        user_id=current_user['id']
    )
    db.session.add(new_workout)
    db.session.commit()

    return jsonify(message="Treino criado com sucesso", workout=workout_data), 201

# Rota para listar treinos (exige autenticação JWT)
@app.route('/api/workouts', methods=['GET'])
@jwt_required()
def get_workouts():
    current_user = get_jwt_identity()  # Obtém o e-mail do usuário logado
    user = User.query.filter_by(email=current_user).first()  # Buscar o usuário no banco de dados
    if user:
        workouts = Workout.query.filter_by(user_id=user.id).all()  # Recuperar os treinos do usuário
        workout_list = [{"name": workout.name, "duration": workout.duration} for workout in workouts]
        return jsonify(workouts=workout_list), 200
    else:
        return jsonify(error="Usuário não encontrado"), 404

# Rota de Logout (opcional, caso precise invalidar o token)
@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    # Para um logout simples com JWT, a única coisa necessária é não enviar mais o token.
    return jsonify(message="Logout bem-sucedido"), 200

# Inicializando o banco de dados
if __name__ == '__main__':
    app.run(debug=True)
