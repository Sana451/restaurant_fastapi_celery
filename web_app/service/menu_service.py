from fastapi import Depends
import uuid

from web_app.repository.menu_repository import MenuRepository  # type: ignore
from project.menus.models import Menu  # type: ignore

from web_app import schemas  # type: ignore
from web_app.repository.pr_repository import PrintRepository  # type: ignore
from web_app.repository.redis_repository import RedisRepository  # type: ignore


class MenuService:
    def __init__(self, db_repository: MenuRepository = Depends(), redis_repository: RedisRepository = Depends()):
        self.db_repository = db_repository
        self.redis_repository = redis_repository
        self.pr_repository = PrintRepository()

    def get_all(self) -> list[Menu]:
        self.redis_repository.get_list_items_from_cash(['1', '2', '3'])
        db_menus = self.db_repository.get_menu_list()
        return db_menus

    def get(self, menu_id: uuid.UUID) -> Menu:
        cash_menu = self.redis_repository.get_item_from_cash(str(menu_id))
        if cash_menu:
            return cash_menu
        db_item = self.db_repository.get_menu(menu_id)
        self.redis_repository.add_item_to_cash(str(menu_id), db_item)
        return db_item

    def create(self, menu: schemas.MenuRequestCreate):
        db_item = self.db_repository.create_menu(menu)
        self.redis_repository.add_item_to_cash(str(db_item.id), db_item)
        return db_item

    def update(self, menu: schemas.MenuRequestCreate, menu_id: uuid.UUID):
        self.redis_repository.del_item_from_cash(str(menu_id))
        db_item = self.db_repository.update_menu(menu, menu_id)
        self.redis_repository.add_item_to_cash(str(menu_id), db_item)
        return db_item

    def delete(self, menu_id: uuid.UUID):
        item = self.db_repository.delete_menu(menu_id)
        self.redis_repository.del_item_from_cash(str(menu_id))
        return item
