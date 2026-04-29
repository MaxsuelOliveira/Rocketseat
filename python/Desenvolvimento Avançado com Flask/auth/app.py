from flask import Flask, request, jsonify
from models.users import User
from database import db
from flask_login import LoginManager, login_user , logout_user , login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "ruGDRVGWCpefKpJtaNqLahcWp4vzhrTp"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@127.0.0.1:3306/flask-crud'

# Configurações do Flask-Login
login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login" # type: ignore

@login_manager.user_loader
def load_user(user_id):
    user = int(user_id)
    return User.query.get(user)

@app.route("/login", methods=["POST"])
def login():
    # Resolve o problema do .get diretamento no data, caso o resquet possa ser Null.
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON inválido ou ausente"}), 400

    username = data.get("username")
    password = data.get("password")

    
    if not username or not password:
        return jsonify({"error": "Usuário e senha são obrigatórios"}), 400
    
    # Lógica para verificar as credenciais do usuário
    if username and password:
        user  = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            login_user(user)
            return jsonify({"message": "Login bem-sucedido", "user": {"id": user.id, "username": user.username}}), 200

    return jsonify({"error": "Credenciais inválidas"}), 400

@app.route("/logout",methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message" : "Usuário deslogado do sistema com sucesso."}), 200

# Create
@app.route("/user", methods=["POST"])
def create_user():
    
    # Resolve o problema do .get diretamento no data, caso o resquet possa ser Null.
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON inválido ou ausente"}), 400

    username = data.get("username")
    password = data.get("password")

    # Validacao inicial 
    if username and password:
        
        # Verificando se existe usuário antes de cadastrar
        user = User.query.filter_by(username=username).first()
        if user :
            return jsonify({"message" : "Usuário já registrado"}), 401
        
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message" : "Usuario cadastrado com sucesso."})
    
    return jsonify({"message" : "dados validos."}) , 401

# Read
@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def get_user_by_id(id_user):
    user = User.query.get(id_user)
    
    if user :
        return jsonify({"username":user.username}), 200
    
    return jsonify({"message" : "Usuário nao encontrado."}), 404

# Update
@app.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
    
    if not id_user:
        return jsonify({"message" : "is_user nao definido"})
    
    # Resolve o problema do .get diretamento no data, caso o resquet possa ser Null.
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON inválido ou ausente"}), 400

    user = User.query.get(id_user)
    password = data.get("password")   
     
    if user and password :
        user.password = password  # type: ignore
        db.session.commit()
        
        return jsonify({"user" : user.username, "message": "A senha do usuário foi atualizada !"}), 200


    return jsonify({"message" : "Usuário nao encontrado."}), 404

# Delete
@app.route("/user/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)
    
    if current_user.id == id_user :
        return jsonify({"message" : "Voce nao pode deletar o seu login."})
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário deletedo com sucesso."}), 200
    
    return jsonify({"message" : "Usuário nao encontrado."}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Caso nao exista o usuario admin ele cria !
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", password="123456")
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)