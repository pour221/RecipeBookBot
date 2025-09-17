from typing import List
from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Recipe(Base):
    __tablename__ = 'recipes'
    recipe_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    collection_id: Mapped[int] = mapped_column(ForeignKey("collections.collection_id"))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    recipe_name: Mapped[str] = mapped_column(String(200))
    descriptions: Mapped[str]

    ingredients_table: Mapped[int | None]
    equipments: Mapped[str | None] = mapped_column(String(250))
    photos: Mapped[str | None] = mapped_column(String(400))
    # nutrition: Mapped[str | None]

    user: Mapped["User"] = relationship(back_populates='recipes')
    collection: Mapped["Collection"] = relationship(back_populates='recipes')
    ingredients: Mapped[List["RecipeIngredient"]] = relationship(back_populates='recipe')


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.recipe_id"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.ingredient_id"))
    amount: Mapped[float] = mapped_column(Float)

    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="recipe")


