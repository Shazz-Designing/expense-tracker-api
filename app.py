from flask import Flask, request, session, jsonify
from config import db, migrate, bcrypt
from models import User, Expense

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super-secret-key'


# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)


@app.route('/')
def home():
    return jsonify(message="Expense Tracker API is running")


# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}

    username = data.get('username')
    password = data.get('password')

    # validate input
    if not username or not password:
        return jsonify(error="Username and password required"), 400

    # check if user exists
    if User.query.filter_by(username=username).first():
        return jsonify(error="Username already exists"), 400

    # create user
    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    # log them in immediately
    session['user_id'] = new_user.id

    return jsonify(message="User created successfully"), 201


# ---------------- LOGIN ----------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    username = data.get('username')
    password = data.get('password')

    # validate input
    if not username or not password:
        return jsonify(error="Username and password required"), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify(message="Login successful"), 200

    return jsonify(error="Invalid credentials"), 401


# ---------------- LOGOUT ----------------
@app.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return jsonify(message="Logged out"), 200


# ---------------- CHECK SESSION ----------------
@app.route('/me', methods=['GET'])
def me():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify(error="Unauthorized"), 401

    user = User.query.get(user_id)

    if not user:
        return jsonify(error="User not found"), 404

    return jsonify(
        id=user.id,
        username=user.username
    ), 200


if __name__ == '__main__':
    app.run(debug=True)