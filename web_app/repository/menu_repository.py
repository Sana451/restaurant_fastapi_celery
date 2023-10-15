import uuid
from collections.abc import Sequence

from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from project.database import get_db  # type: ignore
from web_app import schemas  # type: ignore
from project.menus.models import Menu, SubMenu, Dish  # type: ignore
from sqlalchemy import select, func, distinct


class MenuRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.model = Menu

    def get_menu(self, menu_id: uuid.UUID) -> Menu:
        query = select(Menu,
                       func.count(distinct(SubMenu.id)).label('submenus_count'),
                       func.count(distinct(Dish.id)).label('dishes_count')
                       ).filter_by(id=menu_id
                                   ).outerjoin(SubMenu, Menu.id == SubMenu.menu_id
                                               ).outerjoin(Dish, SubMenu.id == Dish.submenu_id
                                                           ).group_by(Menu.id)

        db_item = self.db.execute(query).first()
        if db_item:
            menu_result = db_item[0]
            menu_result.submenus_count = db_item[1]
            menu_result.dishes_count = db_item[2]
            return menu_result
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    def get_menu_list(self) -> Sequence[Menu]:
        query = select(Menu,
                       func.count(distinct(SubMenu.id)).label('submenus_count'),
                       func.count(distinct(Dish.id)).label('dishes_count')
                       ).outerjoin(SubMenu, Menu.id == SubMenu.menu_id
                                   ).outerjoin(Dish, SubMenu.id == Dish.submenu_id
                                               ).group_by(Menu.id)
        items = self.db.execute(query).all()
        if items is []:
            return items
        result = []
        for item in items:
            item[0].submenus_count = item[1]
            item[0].dishes_count = item[2]
            result.append(item[0])
        return result

    def create_menu(self, menu: schemas.MenuRequestCreate) -> Menu:
        new_menu_db = self.model(id=uuid.uuid4(), title=menu.title, description=menu.description)
        self.db.add(new_menu_db)
        self.db.commit()
        self.db.refresh(new_menu_db)
        return new_menu_db

    def update_menu(self, menu: schemas.MenuRequestCreate, menu_id: uuid.UUID) -> Menu:
        old_menu = self.get_menu(menu_id)
        if old_menu:
            old_menu.title = menu.title
            old_menu.description = menu.description
            self.db.commit()
            self.db.refresh(old_menu)
            return old_menu
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    def delete_menu(self, menu_id: uuid.UUID):
        menu = self.db.scalars(
            select(Menu).filter_by(id=menu_id)
        ).first()
        if menu:
            self.db.delete(menu)
            self.db.commit()
            return {
                "status": True,
                "message": "The menu has been deleted"
            }
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    # def get_menu_id_list(self) -> list[uuid.UUID]:
    #     res = self.db.scalars(select(Menu.id)).all()
    #     return res
