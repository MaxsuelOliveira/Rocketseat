import bcrypt
from flask import Flask, request
from models.users import User
from database import db
from flask_login import LoginManager, login_required, current_user
from controllers.user import UserController

app = Flask(__name__)
app.config['SECRET_KEY'] = "ruGDRVGWCpefKpJtaNqLahcWp4vzhrTp"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:admin123@localhost:3307/minha_dieta"

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
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    password = str.encode(password)
    user = UserController.login_user(username, password)
    return user


@app.route("/logout",methods=["GET"])
@login_required
def logout():
    user = UserController.logout_user()
    return user

# Create
@app.route("/user", methods=["POST"])
def create_user():
    username = request.json.get("username")
    password = request.json.get("password")
    role = request.json.get("role")
    
    user = UserController.create_user(username, password, role)
    return user 


# Read
@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def get_user_by_id(id_user):
    user = UserController.get_user_by_id(id_user)
    return user

# ReadAll
@app.route("/users/", methods=["GET"])
@login_required
def get_all_user():
    users = UserController.get_all_users()
    return users

# Update
@app.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
    password = request.json.get("password")
    password = str.encode(password)
    user = UserController.update_user(id_user, password)
    return user

# Delete
@app.route("/user/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = UserController.delete_user(id_user)
    return user


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Caso nao exista o usuario admin ele cria !
        if not User.query.filter_by(username="admin").first():
            hashed_password = bcrypt.hashpw(str.encode("admin123"), bcrypt.gensalt())
            admin = User(username="admin", password=hashed_password, role="admin")
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)