from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Ingredient(Base):
    __tablename__ = 'ingredients'
    ingredient_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(150))
    kcal: Mapped[int]  # per 100 g
    protein: Mapped[float]
    fat: Mapped[float]
    carbs: Mapped[float]

    recipe: Mapped[List["RecipeIngredient"]] = relationship(back_populates="ingredient")
