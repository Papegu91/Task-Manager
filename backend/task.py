from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # Update this with your database URI
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a strong key

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'completed': self.completed
        }

# Create the database
@app.before_first_request
def create_tables():
    db.create_all()

# Get all tasks for the authenticated user
@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([task.to_dict() for task in tasks]), 200

# Create a new task
@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    user_id = get_jwt_identity()

    task = Task(
        title=data['title'],
        description=data.get('description'),
        due_date=datetime.strptime(data.get('due_date'), '%Y-%m-%d') if data.get('due_date') else None,
        user_id=user_id
    )
    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201

# Get a specific task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task:
        return jsonify(task.to_dict()), 200
    return jsonify({"message": "Task not found"}), 404

# Update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    user_id = get_jwt_identity()

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"message": "Task not found"}), 404

    task.title = data['title']
    task.description = data.get('description')
    task.completed = data.get('completed', task.completed)
    task.due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d') if data.get('due_date') else task.due_date

    db.session.commit()
    return jsonify(task.to_dict()), 200

# Delete a task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
