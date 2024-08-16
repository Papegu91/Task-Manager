@app.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([tag.to_dict() for tag in tags]), 200

@app.route('/tags', methods=['POST'])
def create_tag():
    data = request.get_json()
    tag = Tag(name=data['name'])
    db.session.add(tag)
    db.session.commit()
    return jsonify(tag.to_dict()), 201

@app.route('/tags/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return jsonify(tag.to_dict()), 200

@app.route('/tags/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    data = request.get_json()
    tag = Tag.query.get_or_404(tag_id)
    tag.name = data['name']
    db.session.commit()
    return jsonify(tag.to_dict()), 200

@app.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({"message": "Tag deleted"}), 200
