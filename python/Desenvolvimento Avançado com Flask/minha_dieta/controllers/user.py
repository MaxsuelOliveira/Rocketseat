import bcrypt
from flask import request, jsonify
from flask_login import LoginManager, login_user , logout_user , login_required, current_user
from models.users import User
from database import db

class UserController:
    @staticmethod
    def create_user(username: str, password: bytes, role: str):
        # Resolve o problema do .get diretamento no data, caso o resquet possa ser Null.
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON inválido ou ausente"}), 400

        username = data.get("username")
        password = data.get("password")

        # Validacao inicial 
        if username and password:
            
            # Verificando se existe usuário antes de cadastrar
            hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
            user = User.query.filter_by(username=username).first()
            if user :
                return jsonify({"message" : "Usuário já registrado"}), 401
            
            user = User(username=username, password=hashed_password, role="user")
            db.session.add(user)
            db.session.commit()
            return jsonify(user.to_dict()), 201
        
        return jsonify({"message" : "Dados inválidos ou ausentes."}), 403
     
    @staticmethod
    def get_user_by_id(id_user: int):
        user = User.query.get(id_user)

        if user:
            return jsonify(user.to_dict()), 200
        
        return jsonify({"message" : "Usuário não encontrado."}), 404
    
    @staticmethod
    def get_all_users():
        users = User.query.all()
        return [user.to_dict() for user in users]
    
    @staticmethod
    def login_user(username: str, password: bytes):
        user = User.query.filter_by(username=username).first()
        user_password = str.encode(user.password)
        if user and bcrypt.checkpw(password, user_password):
            return jsonify(user.to_dict()), 200
        return jsonify({"message" : "Usuário ou senha inválidos."}), 401
    
    @staticmethod
    def logout_user():
        logout_user()
        return jsonify({"message" : "Usuário deslogado do sistema com sucesso."}), 200
    
    @staticmethod
    def update_user(id_user: int, password: bytes):
        
        if id_user != current_user.id and current_user.role == "user":
            return jsonify({"message" : "Apenas administradores."}), 403
    
        user = User.query.get(id_user)
        
        if user and password :
            user.password = password  # type: ignore
            db.session.commit()
            return jsonify({"user" : user.username, "message": "A senha do usuário foi atualizada !"}), 200
        
        return jsonify({"message" : "Usuário nao encontrado."}), 404
    
    @staticmethod
    def delete_user(id_user: int):
        
        if id_user != current_user.id and current_user.role == "user":
            return jsonify({"message" : "Apenas administradores."}), 403
    
        user = User.query.get(id_user)
        
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "Usuário deletado com sucesso!"}), 200
        
        return jsonify({"message" : "Usuário nao encontrado."}), 404
    
    
    
    
    
    