from fastapi import Depends
import uuid

from web_app.repository.dish_repository import DishRepository  # type: ignore
from web_app.repository.redis_repository import RedisRepository  # type: ignore
from web_app import schemas  # type: ignore


class DishService:
    def __init__(self, db_repository: DishRepository = Depends(), redis_repository: RedisRepository = Depends()):
        self.db_repository = db_repository
        self.redis_repository = redis_repository

    def get_all(self, submenu_id: uuid.UUID, menu_id: uuid.UUID):
        return self.db_repository.get_dishes_list(submenu_id)

    def get(self, dish_id: uuid.UUID, submenu_id: uuid.UUID, menu_id: uuid.UUID):
        cache_dish = self.redis_repository.get_item_from_cash(str(dish_id))
        if cache_dish:
            return cache_dish
        db_item = self.db_repository.get_dish(dish_id)
        self.redis_repository.add_item_to_cash(str(dish_id), db_item)
        return db_item

    def create(self, dish: schemas.DishRequestCreate, submenu_id: uuid.UUID, menu_id: uuid.UUID):
        self.redis_repository.del_item_from_cash(str(menu_id))
        self.redis_repository.del_item_from_cash(str(submenu_id))
        item = self.db_repository.create_dish(dish, submenu_id)
        self.redis_repository.add_item_to_cash(str(item.id), item)
        return item

    def update(self, dish: schemas.DishRequestCreate, dish_id: uuid.UUID, submenu_id: uuid.UUID, menu_id: uuid.UUID):
        self.redis_repository.del_item_from_cash(str(menu_id))
        self.redis_repository.del_item_from_cash(str(submenu_id))
        self.redis_repository.del_item_from_cash(str(dish_id))
        item = self.db_repository.update_dish(dish, dish_id)
        self.redis_repository.add_item_to_cash(str(dish_id), item)
        return item

    def delete(self, dish_id: uuid.UUID, submenu_id: uuid.UUID, menu_id: uuid.UUID):
        self.redis_repository.del_item_from_cash(str(menu_id))
        self.redis_repository.del_item_from_cash(str(submenu_id))
        self.redis_repository.del_item_from_cash(str(dish_id))
        item = self.db_repository.delete_dish(dish_id)
        return item
