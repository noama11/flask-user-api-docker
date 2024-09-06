from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate  # Import Flask-Migrate

app = Flask(__name__)

# Configuring the database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/yourdatabase'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate
CORS(app)

# Define a simple model for demonstration purposes
class User(db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def json(self):
        return {'id': self.id, 'username': self.username}


@app.route('/')
def home():
    return 'Welcome to the Flask API!'

# Create a simple route
@app.route('/test')
def hello_world():
    return jsonify(message="Hello, World!")

# Another route example to get users
@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_data = [{'id': user.id, 'username': user.username} for user in users]
        return users_data, 200
    except Exception as e:
        return make_response(jsonify({'message': 'error getting users', 'error':str(e)}), 500)

# Route to get a user by ID
@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Query the user by ID
        user = User.query.get(user_id)
        
        # Check if user exists
        if user is None:
            return jsonify({'error': 'User not found'}), 404

        # Return the user data
        return jsonify({
            'id': user.id,
            'username': user.username
        }), 200

    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# Route to create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Check if the necessary data is provided
    if not data or not 'username' in data:
        return jsonify({'error': 'Username is required'}), 400

    try:
        # Check if the username already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400

        # Create a new User object
        new_user = User(username=data['username'])

        # Add the new user to the session and commit to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': f'User {new_user.username} created successfully!'}), 201

    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback the transaction in case of error
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
