from fastapi import Depends
import uuid
from repository.menu_repository import MenuRepository
from repository.submenu_repository import SubMenuRepository
from repository.dish_repository import DishRepository
from repository.pr_repository import PrintRepository
import schemas
from repository.redis_repository import RedisRepository


class MenuService:
    def __init__(self, db_repository: MenuRepository = Depends()):
        self.db_repository = db_repository
        self.pr_repository = PrintRepository()
        self.redis_repository = RedisRepository()

    def get_all(self):
        return self.db_repository.get_menu_list()

    def get(self, menu_id: uuid.UUID):
        # cash = self.redis_repository.get_from_cash(str(menu_id))
        # if cash:
        #     print("i am from redis: ", cash)
        #     return cash
        db_item = self.db_repository.get_menu(menu_id)
        # print("i am from db: ", db_item)
        # self.redis_repository.add_to_cash(str(menu_id), db_item)
        return db_item

    def create(self, menu: schemas.MenuRequestCreate):
        # self.pr_repository.print_something()
        item = self.db_repository.create_menu(menu)
        return item

    def update(self, menu: schemas.MenuRequestCreate, menu_id: uuid.UUID):
        db_item = self.db_repository.update_menu(menu, menu_id)
        self.redis_repository.add_to_cash(str(menu_id), db_item)
        return db_item

    def delete(self, menu_id: uuid.UUID):
        item = self.db_repository.delete_menu(menu_id)
        return item


class SubMenuService:
    def __init__(self, db_repository: SubMenuRepository = Depends()):
        self.db_repository = db_repository

    def get_all(self, menu_id: uuid.UUID):
        return self.db_repository.get_submenu_list(menu_id)

    def get(self, submenu_id: uuid.UUID, menu_id: uuid.UUID):
        return self.db_repository.get_submenu(submenu_id, menu_id)

    def create(self, submenu: schemas.SubMenuRequestCreate, menu_id: uuid.UUID):
        item = self.db_repository.create_submenu(submenu, menu_id)
        return item

    def update(self, submenu: schemas.SubMenuRequestCreate, submenu_id: uuid.UUID, menu_id: uuid.UUID):
        item = self.db_repository.update_submenu(submenu, submenu_id, menu_id)
        return item

    def delete(self, submenu_id: uuid.UUID):
        item = self.db_repository.delete_submenu(submenu_id)
        return item


class DishService:
    def __init__(self, db_repository: DishRepository = Depends()):
        self.db_repository = db_repository

    def get_all(self, submenu_id: uuid.UUID):
        return self.db_repository.get_dishes_list(submenu_id)

    def get(self, dish_id: uuid.UUID):
        return self.db_repository.get_dish(dish_id)

    def create(self, dish: schemas.DishRequestCreate, submenu_id: uuid.UUID):
        item = self.db_repository.create_dish(dish, submenu_id)
        return item

    def update(self, dish: schemas.DishRequestCreate, dish_id: uuid.UUID):
        item = self.db_repository.update_dish(dish, dish_id)
        return item

    def delete(self, dish_id: uuid.UUID):
        item = self.db_repository.delete_dish(dish_id)
        return item
