import uuid  # type: ignore
from collections.abc import Sequence

from fastapi import Depends, status, HTTPException  # type: ignore
from sqlalchemy import select  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from web_app import schemas  # type: ignore
from project.database import get_db  # type: ignore
from project.menus.models import Dish  # type: ignore


class DishRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.model = Dish

    def get_dish(self, dish_id: uuid.UUID) -> Dish:
        item = self.db.scalars(
            select(Dish).filter_by(id=dish_id)
        ).first()
        if item:
            return item
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")

    def get_dishes_list(self, submenu_id: uuid.UUID) -> Sequence[Dish]:
        return self.db.scalars(
            select(Dish).where(Dish.submenu_id == submenu_id)
        ).all()

    def create_dish(self, dish: schemas.DishRequestCreate, submenu_id: uuid.UUID) -> Dish:
        new_dish = self.model(id=uuid.uuid4(), title=dish.title, description=dish.description, price=dish.price,
                              submenu_id=submenu_id)
        self.db.add(new_dish)
        self.db.commit()
        self.db.refresh(new_dish)
        return new_dish

    def update_dish(self, dish: schemas.DishRequestCreate, dish_id: uuid.UUID) -> Dish:
        old_dish = self.get_dish(dish_id)
        if old_dish:
            old_dish.title = dish.title
            old_dish.description = dish.description
            old_dish.price = dish.price
            self.db.commit()
            self.db.refresh(old_dish)
        return old_dish

    def delete_dish(self, dish_id: uuid.UUID):
        dish = self.db.get(self.model, dish_id)
        if dish:
            self.db.delete(dish)
            self.db.commit()
            return {
                "status": True,
                "message": "The dish has been deleted"
            }
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
