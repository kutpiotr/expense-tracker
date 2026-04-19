from pydantic import BaseModel, Field, field_validator
import re
from datetime import date
from decimal import Decimal


HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


class CategoryCreate(BaseModel):
    """Dane wejściowe przy tworzeniu kategorii (POST)."""

    name: str = Field(min_length=1, max_length=50)
    color: str = Field(default="#888888")

    @field_validator("name")
    @classmethod
    def name_stripped(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name cannot be empty or whitespace only")
        return v

    @field_validator("color")
    @classmethod
    def color_is_hex(cls, v: str) -> str:
        if not HEX_COLOR_RE.match(v):
            raise ValueError("color must be a hex code in format #RRGGBB")
        return v


class CategoryUpdate(BaseModel):
    """Dane wejściowe przy edycji kategorii (PUT).
    Wszystkie pola opcjonalne — użytkownik może zmienić tylko kolor albo tylko nazwę.
    """

    name: str | None = Field(default=None, min_length=1, max_length=50)
    color: str | None = None

    @field_validator("name")
    @classmethod
    def name_stripped(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        if not v:
            raise ValueError("name cannot be empty or whitespace only")
        return v

    @field_validator("color")
    @classmethod
    def color_is_hex(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if not HEX_COLOR_RE.match(v):
            raise ValueError("color must be a hex code in format #RRGGBB")
        return v


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    transaction_date: date
    description: str = Field(default="", max_length=255)
    category_id: int = Field(gt=0)

    @field_validator("description")
    @classmethod
    def description_stripped(cls, v: str) -> str:
        return v.strip()


class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    transaction_date: date | None = None
    description: str | None = Field(default=None, max_length=255)
    category_id: int | None = Field(default=None, gt=0)

    @field_validator("description")
    @classmethod
    def description_stripped(cls, v: str | None) -> str | None:
        return v.strip() if v is not None else None


from typing import Literal
from datetime import date


class MonthlyStatsParams(BaseModel):
    year: int = Field(ge=2000, le=2100)
    month: int = Field(ge=1, le=12)


class DateRangeParams(BaseModel):
    date_from: date | None = None
    date_to: date | None = None


class TrendParams(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    granularity: Literal["day", "month"] = "day"
