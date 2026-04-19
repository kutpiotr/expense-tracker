from flask import Blueprint, jsonify

bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@bp.route("", methods=["GET"])
def list_categories():
    from app.models import Category  # import wewnątrz funkcji — bezpieczny

    categories = Category.query.order_by(Category.name).all()
    return jsonify([c.to_dict() for c in categories])
