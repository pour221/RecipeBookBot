from datetime import datetime
from typing import List
from sqlalchemy import BigInteger, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base

class Ingredient:
    __tablename__ = 'ingredients'
    ingredient_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(150))
    kcal: Mapped[int]  # на 100 г
    protein: Mapped[float]  # на 100 г
    fat: Mapped[float]  # на 100 г
    carbs: Mapped[float]  # на 100 г

    recipe: Mapped[List["RecipeIngredient"]] = relationship(back_populates="ingredient")
