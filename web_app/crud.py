import uuid

from sqlalchemy.orm import Session

import models  # type: ignore
import schemas  # type: ignore


def get_menu_by_id(db: Session, menu_id: uuid.UUID):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()


def get_submenu_by_id(db: Session, submenu_id: uuid.UUID):
    return db.query(models.SubMenu).where(models.SubMenu.id == submenu_id).first()


def get_dish_by_id(db: Session, dish_id: uuid.UUID):
    return db.query(models.Dish).where(models.Dish.id == dish_id).first()


def get_menu_list(db: Session):
    return db.query(models.Menu).all()


def get_submenu_list(db: Session, menu_id: uuid.UUID):
    return db.query(models.SubMenu).filter(models.SubMenu.menu_id == menu_id).all()


def get_dishes_list(db: Session, submenu_id: uuid.UUID):
    return db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all()


def create_menu(db: Session, menu: schemas.MenuRequestCreate):
    new_menu_db = models.Menu(id=uuid.uuid4(), title=menu.title, description=menu.description)
    db.add(new_menu_db)
    db.commit()
    db.refresh(new_menu_db)
    return new_menu_db


def create_submenu(db: Session, submenu: schemas.SubMenuRequestCreate, menu_id: uuid.UUID):
    new_submenu_db = models.SubMenu(id=uuid.uuid4(), title=submenu.title, description=submenu.description,
                                    menu_id=menu_id)
    db.add(new_submenu_db)
    db.commit()
    db.refresh(new_submenu_db)
    return new_submenu_db


def create_dish(db: Session, dish: schemas.DishRequestCreate, submenu_id: uuid.UUID):
    new_dish_db = models.Dish(title=dish.title, description=dish.description, price=dish.price, submenu_id=submenu_id)
    db.add(new_dish_db)
    db.commit()
    db.refresh(new_dish_db)
    return new_dish_db


def update_menu(db: Session, menu: schemas.MenuRequestCreate, menu_id: uuid.UUID):
    old_menu = get_menu_by_id(db, menu_id)
    if old_menu:
        old_menu.title = menu.title
        old_menu.description = menu.description
        db.commit()
    return old_menu


def update_submenu(db: Session, submenu: schemas.MenuRequestCreate, submenu_id: uuid.UUID):
    old_submenu = get_submenu_by_id(db, submenu_id)
    if old_submenu:
        old_submenu.title = submenu.title
        old_submenu.description = submenu.description
        db.commit()
    return old_submenu


def update_dish(db: Session, dish: schemas.DishRequestCreate, dish_id: uuid.UUID):
    old_dish = get_dish_by_id(db, dish_id)
    if old_dish:
        old_dish.title = dish.title
        old_dish.description = dish.description
        old_dish.price = dish.price
        db.commit()
    return old_dish


def delete_menu(db: Session, menu_id: uuid.UUID):
    menu = get_menu_by_id(db, menu_id)
    if menu:
        db.delete(menu)
        db.commit()
        return True


def delete_submenu(db: Session, submenu_id: uuid.UUID):
    submenu = get_submenu_by_id(db, submenu_id)
    if submenu:
        db.delete(submenu)
        db.commit()
        return True


def delete_dish(db: Session, dish_id: uuid.UUID):
    dish = get_dish_by_id(db, dish_id)
    if dish:
        db.delete(dish)
        db.commit()
        return True
