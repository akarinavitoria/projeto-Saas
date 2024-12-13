from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

# Configuração do JWT
app.config["JWT_SECRET_KEY"] = "sua_chave_secreta_segura"
jwt = JWTManager(app)

# Ativando o CORS para permitir conexões do frontend
CORS(app)

# Armazenamento temporário de clientes e treinos (simulando um banco de dados)
clients = []

users = [
    {"id": 1, "username": "admin", "password": "admin123"}  # Usuário fictício
]

# Rotas de autenticação
@app.route('/api/login', methods=['POST'])
def login():
    credentials = request.json
    user = next((u for u in users if u["username"] == credentials.get("username") and u["password"] == credentials.get("password")), None)
    if not user:
        return jsonify({"error": "Credenciais inválidas."}), 401
    access_token = create_access_token(identity=user["id"])
    return jsonify({"access_token": access_token}), 200

# Rotas de clientes
@app.route('/api/clients', methods=['POST'])
@jwt_required()
def add_client():
    try:
        new_client = request.json
        if not new_client.get("name") or not new_client.get("email"):
            return jsonify({"error": "Os campos 'name' e 'email' são obrigatórios."}), 400
        new_client["id"] = len(clients) + 1
        clients.append(new_client)
        return jsonify(new_client), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao adicionar cliente: {str(e)}"}), 500

@app.route('/')
def home():
    return jsonify({"message": "API do projeto de academias está rodando!"}), 200


# Rota inicial
@app.route('/')
def home():
    return jsonify({"message": "API do Gym Manager está rodando!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

