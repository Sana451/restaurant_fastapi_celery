from fastapi import Depends
import uuid
from web_app.repository.submenu_repository import SubMenuRepository  # type: ignore
from web_app.repository.redis_repository import RedisRepository  # type: ignore
from web_app import schemas  # type: ignore


class SubMenuService:
    def __init__(self, db_repository: SubMenuRepository = Depends(), redis_repository: RedisRepository = Depends()):
        self.db_repository = db_repository
        self.redis_repository = redis_repository

    def get_all(self, menu_id: uuid.UUID):
        return self.db_repository.get_submenu_list(menu_id)

    def get(self, submenu_id: uuid.UUID, menu_id: uuid.UUID):
        cache_submenu = self.redis_repository.get_item_from_cash(str(submenu_id))
        if cache_submenu:
            return cache_submenu
        db_item = self.db_repository.get_submenu(submenu_id, menu_id)
        self.redis_repository.add_item_to_cash(str(submenu_id), db_item)
        return db_item

    def create(self, submenu: schemas.SubMenuRequestCreate, menu_id: uuid.UUID):
        self.redis_repository.del_item_from_cash(str(menu_id))
        item = self.db_repository.create_submenu(submenu, menu_id)
        self.redis_repository.add_item_to_cash(str(item.id), item)
        return item

    def update(self, submenu: schemas.SubMenuRequestCreate, submenu_id: uuid.UUID, menu_id: uuid.UUID):
        self.redis_repository.del_item_from_cash(str(submenu_id))
        item = self.db_repository.update_submenu(submenu, submenu_id, menu_id)
        self.redis_repository.add_item_to_cash(str(submenu_id), item)
        return item

    def delete(self, submenu_id: uuid.UUID, menu_id: uuid.UUID):
        self.redis_repository.del_item_from_cash(str(menu_id))
        self.redis_repository.del_item_from_cash(str(submenu_id))
        item = self.db_repository.delete_submenu(submenu_id)
        return item
