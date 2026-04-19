from datetime import date
from flask import Blueprint, jsonify, request
from sqlalchemy import and_
from app.extensions import db
from app.models import Transaction, Category
from app.schemas import TransactionCreate, TransactionUpdate

bp = Blueprint("transactions", __name__, url_prefix="/api/transactions")


def _parse_date(value: str | None) -> date | None:
    """Helper do parsowania query params ?from=... &to=..."""
    if value is None:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"invalid date format: {value!r}, expected YYYY-MM-DD")


@bp.route("", methods=["GET"])
def list_transactions():
    # Query parameters — wszystkie opcjonalne
    date_from = _parse_date(request.args.get("from"))
    date_to = _parse_date(request.args.get("to"))
    category_id = request.args.get("category_id", type=int)
    search = request.args.get("q")

    query = Transaction.query

    if date_from is not None:
        query = query.filter(Transaction.transaction_date >= date_from)
    if date_to is not None:
        query = query.filter(Transaction.transaction_date <= date_to)
    if category_id is not None:
        query = query.filter(Transaction.category_id == category_id)
    if search:
        query = query.filter(Transaction.description.ilike(f"%{search}%"))

    # Najnowsze pierwsze; przy równych datach — najnowsze utworzone
    query = query.order_by(
        Transaction.transaction_date.desc(), Transaction.created_at.desc()
    )

    transactions = query.all()
    return jsonify([t.to_dict() for t in transactions])


@bp.route("/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id: int):
    transaction = db.session.get(Transaction, transaction_id)
    if transaction is None:
        return (
            jsonify(
                {
                    "error": "not_found",
                    "message": f"transaction {transaction_id} not found",
                }
            ),
            404,
        )
    return jsonify(transaction.to_dict())


@bp.route("", methods=["POST"])
def create_transaction():
    payload = TransactionCreate.model_validate(request.get_json() or {})

    # Sprawdź, że wskazana kategoria istnieje — FK by i tak zadziałał,
    # ale lepszy komunikat błędu niż generyczny IntegrityError
    category = db.session.get(Category, payload.category_id)
    if category is None:
        return (
            jsonify(
                {
                    "error": "invalid_reference",
                    "message": f"category {payload.category_id} does not exist",
                }
            ),
            400,
        )

    transaction = Transaction(
        amount=payload.amount,
        transaction_date=payload.transaction_date,  # <-- zmienione
        description=payload.description,
        category_id=payload.category_id,
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify(transaction.to_dict()), 201


@bp.route("/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id: int):
    transaction = db.session.get(Transaction, transaction_id)
    if transaction is None:
        return (
            jsonify(
                {
                    "error": "not_found",
                    "message": f"transaction {transaction_id} not found",
                }
            ),
            404,
        )

    payload = TransactionUpdate.model_validate(request.get_json() or {})

    if payload.category_id is not None:
        if db.session.get(Category, payload.category_id) is None:
            return (
                jsonify(
                    {
                        "error": "invalid_reference",
                        "message": f"category {payload.category_id} does not exist",
                    }
                ),
                400,
            )
        transaction.category_id = payload.category_id
    if payload.amount is not None:
        transaction.amount = payload.amount
    if payload.transaction_date is not None:
        transaction.transaction_date = payload.transaction_date
    if payload.description is not None:
        transaction.description = payload.description

    db.session.commit()
    return jsonify(transaction.to_dict())


@bp.route("/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id: int):
    transaction = db.session.get(Transaction, transaction_id)
    if transaction is None:
        return (
            jsonify(
                {
                    "error": "not_found",
                    "message": f"transaction {transaction_id} not found",
                }
            ),
            404,
        )

    db.session.delete(transaction)
    db.session.commit()
    return "", 204
