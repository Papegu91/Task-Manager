from flask import Blueprint, request, jsonify
from app import db, jwt
from models import User, Task, Tag, TaskTag
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

auth_bp = Blueprint('auth', __name__)
task_bp = Blueprint('tasks', __name__)
tag_bp = Blueprint('tags', __name__)
user_bp = Blueprint('user', __name__)

# Auth routes
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"message": "User logged out"}), 200

# User routes
@user_bp.route('/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "username": user.username,
            "email": user.email
        }), 200
    return jsonify({"message": "User not found"}), 404

# Task routes
@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([task.to_dict() for task in tasks]), 200

@task_bp.route('/tasks', methods=['POST'])
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

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task:
        return jsonify(task.to_dict()), 200
    return jsonify({"message": "Task not found"}), 404

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
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

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200

# Tag routes
@tag_bp.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([tag.to_dict() for tag in tags]), 200

@tag_bp.route('/tags', methods=['POST'])
def create_tag():
    data = request.get_json()
    tag = Tag(name=data['name'])
    db.session.add(tag)
    db.session.commit()
    return jsonify(tag.to_dict()), 201

@tag_bp.route('/tags/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return jsonify(tag.to_dict()), 200

@tag_bp.route('/tags/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    data = request.get_json()
    tag = Tag.query.get_or_404(tag_id)
    tag.name = data['name']
    db.session.commit()
    return jsonify(tag.to_dict()), 200

@tag_bp.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({"message": "Tag deleted"}), 200
