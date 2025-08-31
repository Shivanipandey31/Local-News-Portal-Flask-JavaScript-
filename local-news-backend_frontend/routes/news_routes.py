from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.article import Article

news_bp = Blueprint("news", __name__)

# Create Article (JWT required)
@news_bp.route("/articles", methods=["POST"])
@jwt_required()
def add_article():
    data = request.get_json() or {}
    title = data.get("title")
    content = data.get("content")
    source = data.get("source")

    if not title or not content or not source:
        return jsonify({"success": False, "error": "Title, content, and source are required"}), 400

    # identity was stored as string during login
    user_id = int(get_jwt_identity())

    article = Article(title=title, content=content, source=source, user_id=user_id)
    db.session.add(article)
    db.session.commit()
    return jsonify({"success": True, "data": article.to_dict()}), 201

# Get all articles (public, paginated)
@news_bp.route("/articles", methods=["GET"])
def get_articles():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = Article.query.order_by(Article.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        "success": True,
        "data": [a.to_dict() for a in pagination.items],
        "page": pagination.page,
        "total_pages": pagination.pages,
        "total_articles": pagination.total
    }), 200

# Get single article (public)
@news_bp.route("/articles/<int:article_id>", methods=["GET"])
def get_article(article_id):
    article = Article.query.get_or_404(article_id)
    return jsonify({"success": True, "data": article.to_dict()}), 200

# Update (JWT required, author-only)
@news_bp.route("/articles/<int:article_id>", methods=["PUT"])
@jwt_required()
def update_article(article_id):
    article = Article.query.get_or_404(article_id)
    current_user_id = int(get_jwt_identity())
    if article.user_id != current_user_id:
        return jsonify({"success": False, "error": "Not authorized to update this article"}), 403

    data = request.get_json() or {}
    article.title = data.get("title", article.title)
    article.content = data.get("content", article.content)
    article.source = data.get("source", article.source)

    db.session.commit()
    return jsonify({"success": True, "data": article.to_dict()}), 200

# Delete (JWT required, author-only)
@news_bp.route("/articles/<int:article_id>", methods=["DELETE"])
@jwt_required()
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    current_user_id = int(get_jwt_identity())
    if article.user_id != current_user_id:
        return jsonify({"success": False, "error": "Not authorized to delete this article"}), 403

    db.session.delete(article)
    db.session.commit()
    return jsonify({"success": True, "message": "Article deleted"}), 200
