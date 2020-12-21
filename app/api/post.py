import json

from flask import jsonify, request
from app.api import bp

from app.models import User, Post
from app import db


@bp.route('/posts', methods=['GET'])
def get_posts():
    limit = min(request.args.get('limit', 10, int), 100)
    offset = (request.args.get('page', 1, int) - 1) * request.args.get('limit', 10, int)
    return jsonify([post.to_dict() for post in Post.query.limit(limit).offset(offset).all()])


@bp.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    return jsonify(Post.query.get_or_404(id).to_dict())


@bp.route('/posts', methods=['POST'])
def add_post():
    data = request.get_json() or {}
    post = Post()
    post.from_dict(**data)
    user = User.query.get_or_404(data['user_id'])
    user.posts.append(post)
    db.session.commit()
    return jsonify(post.to_dict())


@bp.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get_or_404(id)
    data = request.get_json() or {}
    post.from_dict(**data)
    db.session.commit()
    return jsonify(post.to_dict())


@bp.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'ok'})
