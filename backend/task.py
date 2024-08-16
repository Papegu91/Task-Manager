@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([task.to_dict() for task in tasks]), 200

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

@app.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task:
        return jsonify(task.to_dict()), 200
    return jsonify({"message": "Task not found"}), 404

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
