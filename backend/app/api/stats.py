from datetime import date
from flask import Blueprint, jsonify, request
from sqlalchemy import func, and_
from app.extensions import db
from app.models import Transaction, Category
from app.schemas import MonthlyStatsParams, DateRangeParams, TrendParams
from app.api.stats_helpers import current_month_range, month_range

bp = Blueprint("stats", __name__, url_prefix="/api/stats")


@bp.route("/summary", methods=["GET"])
def monthly_summary():
    """Podsumowanie pojedynczego miesiąca.
    Bez parametrów → bieżący miesiąc. Z ?year=YYYY&month=M → wskazany miesiąc.
    """
    if request.args:
        params = MonthlyStatsParams.model_validate(request.args.to_dict())
        date_from, date_to = month_range(params.year, params.month)
    else:
        date_from, date_to = current_month_range()

    # Jedno zapytanie, kilka agregacji naraz
    result = (
        db.session.query(
            func.coalesce(func.sum(Transaction.amount), 0).label("total"),
            func.count(Transaction.id).label("count"),
            func.coalesce(func.avg(Transaction.amount), 0).label("average"),
            func.count(func.distinct(Transaction.transaction_date)).label(
                "days_with_expenses"
            ),
        )
        .filter(
            Transaction.transaction_date >= date_from,
            Transaction.transaction_date <= date_to,
        )
        .one()
    )

    return jsonify(
        {
            "period": {
                "from": date_from.isoformat(),
                "to": date_to.isoformat(),
            },
            "total": str(result.total),
            "count": result.count,
            "average": str(round(result.average, 2)) if result.count else "0.00",
            "days_with_expenses": result.days_with_expenses,
        }
    )


@bp.route("/by-category", methods=["GET"])
def by_category():
    """Rozkład wydatków na kategorie w zadanym zakresie.
    Bez parametrów → bieżący miesiąc. Wszystkie kategorie są zwracane,
    nawet jeśli nie mają wydatków w danym okresie (total=0).
    """
    if request.args:
        params = DateRangeParams.model_validate(request.args.to_dict())
        date_from = params.date_from
        date_to = params.date_to
    else:
        date_from, date_to = current_month_range()

    # Filtry daty przenoszone do klauzuli ON joina,
    # dzięki czemu kategorie bez wydatków w okresie też się pojawiają (total=0)
    join_conditions = [Transaction.category_id == Category.id]
    if date_from is not None:
        join_conditions.append(Transaction.transaction_date >= date_from)
    if date_to is not None:
        join_conditions.append(Transaction.transaction_date <= date_to)

    query = db.session.query(
        Category.id.label("category_id"),
        Category.name.label("category_name"),
        Category.color.label("category_color"),
        func.coalesce(func.sum(Transaction.amount), 0).label("total"),
        func.count(Transaction.id).label("count"),
    ).outerjoin(
        Transaction, and_(*join_conditions)  # warunki w ON, nie w WHERE
    )

    query = query.group_by(Category.id, Category.name, Category.color)
    query = query.order_by(func.sum(Transaction.amount).desc().nullslast())

    rows = query.all()

    # Policz łączną sumę, żeby dać procent każdej kategorii
    total_sum = (
        sum(float(r.total) for r in rows) or 1
    )  # ochrona przed dzieleniem przez zero

    return jsonify(
        [
            {
                "category_id": r.category_id,
                "category_name": r.category_name,
                "category_color": r.category_color,
                "total": str(r.total),
                "count": r.count,
                "percentage": round(float(r.total) / total_sum * 100, 2),
            }
            for r in rows
        ]
    )


@bp.route("/trend", methods=["GET"])
def trend():
    """Wydatki w czasie.
    granularity=day → suma wydatków per dzień
    granularity=month → suma wydatków per miesiąc (YYYY-MM)
    """
    if request.args:
        params = TrendParams.model_validate(request.args.to_dict())
        date_from = params.date_from
        date_to = params.date_to
        granularity = params.granularity
    else:
        date_from, date_to = current_month_range()
        granularity = "day"

    # Dla grupowania per miesiąc — wyciągamy "YYYY-MM" ze stringa daty
    # SQLite używa strftime, Postgres używałby to_char albo date_trunc
    if granularity == "month":
        period_expr = func.strftime("%Y-%m", Transaction.transaction_date)
    else:
        period_expr = func.strftime("%Y-%m-%d", Transaction.transaction_date)

    query = db.session.query(
        period_expr.label("period"),
        func.sum(Transaction.amount).label("total"),
        func.count(Transaction.id).label("count"),
    )

    if date_from is not None:
        query = query.filter(Transaction.transaction_date >= date_from)
    if date_to is not None:
        query = query.filter(Transaction.transaction_date <= date_to)

    query = query.group_by(period_expr).order_by(period_expr)

    rows = query.all()

    return jsonify(
        {
            "granularity": granularity,
            "period": {
                "from": date_from.isoformat() if date_from else None,
                "to": date_to.isoformat() if date_to else None,
            },
            "data": [
                {
                    "period": r.period,
                    "total": str(r.total),
                    "count": r.count,
                }
                for r in rows
            ],
        }
    )
