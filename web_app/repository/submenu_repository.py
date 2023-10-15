import uuid
from collections.abc import Sequence

from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from web_app import schemas  # type: ignore
from project.database import get_db  # type: ignore
from project.menus.models import SubMenu, Dish  # type: ignore
from sqlalchemy import select, func, distinct


class SubMenuRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.model = SubMenu

    def get_submenu(self, submenu_id: uuid.UUID, menu_id: uuid.UUID) -> SubMenu:
        query = select(SubMenu,
                       func.count(distinct(Dish.id)).label('dishes_count')
                       ).filter_by(id=submenu_id
                                   ).where(SubMenu.menu_id == menu_id
                                           ).outerjoin(Dish, Dish.submenu_id == SubMenu.id
                                                       ).group_by(SubMenu.id)
        item = self.db.scalars(query).first()
        if item:
            item.dishes_count = len(item.dishes)
            return item
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    def get_submenu_list(self, menu_id: uuid.UUID) -> Sequence[SubMenu]:
        query = select(SubMenu,
                       func.count(distinct(Dish.id)).label('dishes_count')
                       ).where(SubMenu.menu_id == menu_id
                               ).outerjoin(Dish, Dish.submenu_id == SubMenu.id
                                           ).group_by(SubMenu.id)
        items = self.db.execute(query).all()
        if items is []:
            return items
        result = []
        for item in items:
            item[0].dishes_count = item[1]
            result.append(item[0])
        return result

    def create_submenu(self, submenu: schemas.SubMenuRequestCreate, menu_id: uuid.UUID) -> SubMenu:
        new_submenu = self.model(id=uuid.uuid4(), title=submenu.title, description=submenu.description, menu_id=menu_id)
        self.db.add(new_submenu)
        self.db.commit()
        self.db.refresh(new_submenu)
        return new_submenu

    def update_submenu(self, submenu: schemas.SubMenuRequestCreate, submenu_id: uuid.UUID,
                       menu_id: uuid.UUID) -> SubMenu:
        old_submenu = self.get_submenu(submenu_id, menu_id)
        print(old_submenu)
        if old_submenu:
            # item_db = self.db.scalars(
            #     select(SubMenu).filter_by(id=submenu_id)
            # ).first()
            old_submenu.title = submenu.title
            # old_submenu.description = submenu.description
            old_submenu.description = submenu.description
            self.db.commit()
            self.db.refresh(old_submenu)
            return old_submenu
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    def delete_submenu(self, submenu_id: uuid.UUID):
        submenu = self.db.scalars(
            select(SubMenu).filter_by(id=submenu_id)
        ).first()
        if submenu:
            self.db.delete(submenu)
            self.db.commit()
            return {
                "status": True,
                "message": "The submenu has been deleted"
            }
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
