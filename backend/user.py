@app.route('/user/profile', methods=['GET'])
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
