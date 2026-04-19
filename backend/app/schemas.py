from pydantic import BaseModel, Field, field_validator
import re

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
