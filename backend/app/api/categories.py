from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Category
from app.schemas import CategoryCreate, CategoryUpdate

bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@bp.route("", methods=["GET"])
def list_categories():
    categories = Category.query.order_by(Category.name).all()
    return jsonify([c.to_dict() for c in categories])


@bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id: int):
    category = db.session.get(Category, category_id)
    if category is None:
        return (
            jsonify(
                {"error": "not_found", "message": f"category {category_id} not found"}
            ),
            404,
        )
    return jsonify(category.to_dict())


@bp.route("", methods=["POST"])
def create_category():
    payload = CategoryCreate.model_validate(request.get_json() or {})
    category = Category(name=payload.name, color=payload.color)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


@bp.route("/<int:category_id>", methods=["PUT"])
def update_category(category_id: int):
    category = db.session.get(Category, category_id)
    if category is None:
        return (
            jsonify(
                {"error": "not_found", "message": f"category {category_id} not found"}
            ),
            404,
        )

    payload = CategoryUpdate.model_validate(request.get_json() or {})

    if payload.name is not None:
        category.name = payload.name
    if payload.color is not None:
        category.color = payload.color

    db.session.commit()
    return jsonify(category.to_dict())


@bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category(category_id: int):
    category = db.session.get(Category, category_id)
    if category is None:
        return (
            jsonify(
                {"error": "not_found", "message": f"category {category_id} not found"}
            ),
            404,
        )

    db.session.delete(category)
    db.session.commit()
    return "", 204
