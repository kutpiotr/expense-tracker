from datetime import datetime, date
from decimal import Decimal
from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(7), nullable=False, default="#888888")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relacja zwrotna — dzięki temu możesz pisać category.transactions
    transactions = db.relationship(
        "Transaction",
        back_populates="category",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Category {self.name}>"


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    transaction_date = db.Column(db.Date, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False, default="")
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    category = db.relationship("Category", back_populates="transactions")

    def to_dict(self):
        return {
            "id": self.id,
            "amount": str(self.amount),
            "transaction_date": self.transaction_date.isoformat(),  # <-- zmienione z "date"
            "description": self.description,
            "category_id": self.category_id,
            "category": (
                {
                    "id": self.category.id,
                    "name": self.category.name,
                    "color": self.category.color,
                }
                if self.category
                else None
            ),
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Transaction {self.amount} on {self.transaction_date}>"
