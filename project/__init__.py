import uuid

from fastapi import FastAPI, Depends, status

from project.celery_utils import create_celery
from web_app import schemas
from web_app.service.menu_service import MenuService
from web_app.service.submenu_service import SubMenuService
from web_app.service.dish_service import DishService


def create_app() -> FastAPI:
    app = FastAPI()

    app.celery_app = create_celery()

    from project.menus import api_v1_router
    app.include_router(api_v1_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.post("/api/v1/menus", status_code=status.HTTP_201_CREATED, response_model=schemas.MenuRequest)
    def create_menu(new_menu: schemas.MenuRequestCreate, menu: MenuService = Depends()):
        return menu.create(new_menu)

    @app.get("/api/v1/menus/{menu_id}", response_model=schemas.MenuRequest)
    def read_menu(menu_id: uuid.UUID, menu: MenuService = Depends()):
        menu_item_db = menu.get(menu_id)
        return menu_item_db

    @app.get("/api/v1/menus", response_model=list[schemas.MenuRequest])
    def read_menu_list(menu: MenuService = Depends()):
        return menu.get_all()

    @app.patch("/api/v1/menus/{menu_id}", response_model=schemas.MenuRequest)
    def update_menu(menu_id: uuid.UUID, new_menu_data: schemas.MenuRequestCreate, menu: MenuService = Depends()):
        updated_menu = menu.update(new_menu_data, menu_id)
        return updated_menu

    @app.delete("/api/v1/menus/{menu_id}", status_code=status.HTTP_200_OK)
    def delete_menu(menu_id: uuid.UUID, menu: MenuService = Depends()):
        deleted_menu = menu.delete(menu_id)
        return deleted_menu

    @app.post("/api/v1/menus/{menu_id}/submenus", status_code=status.HTTP_201_CREATED,
              response_model=schemas.SubMenuRequest)
    def create_submenu(menu_id: uuid.UUID, new_submenu: schemas.SubMenuRequestCreate,
                       submenu: SubMenuService = Depends()):
        return submenu.create(new_submenu, menu_id)

    @app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenuRequest)
    def read_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID, submenu: SubMenuService = Depends()):
        submenu_item_db = submenu.get(submenu_id, menu_id)
        return submenu_item_db

    @app.get("/api/v1/menus/{menu_id}/submenus", response_model=list[schemas.SubMenuRequest])
    def read_submenu_list(menu_id: uuid.UUID, submenu: SubMenuService = Depends()):
        return submenu.get_all(menu_id)

    @app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenuRequest)
    def update_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID, updated_submenu: schemas.MenuRequestCreate,
                       submenu: SubMenuService = Depends()):
        updated_submenu = submenu.update(updated_submenu, submenu_id, menu_id)
        return updated_submenu

    @app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}", status_code=status.HTTP_200_OK)
    def delete_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID, submenu: SubMenuService = Depends()):
        deleted_submenu = submenu.delete(submenu_id, menu_id)
        return deleted_submenu

    @app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=status.HTTP_201_CREATED,
              response_model=schemas.DishRequest)
    def create_dish(menu_id: uuid.UUID, submenu_id: uuid.UUID, new_dish: schemas.DishRequestCreate,
                    dish: DishService = Depends()):
        return dish.create(new_dish, submenu_id, menu_id)

    @app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.DishRequest)
    def read_dish(menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID, dish: DishService = Depends()):
        return dish.get(dish_id, submenu_id, menu_id)

    @app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[schemas.DishRequest])
    def read_dishes_list(menu_id: uuid.UUID, submenu_id: uuid.UUID, dish: DishService = Depends()):
        return dish.get_all(submenu_id, menu_id)

    @app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.DishRequest)
    def update_dish(menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID,
                    updated_dish: schemas.DishRequestCreate,
                    dish: DishService = Depends()):
        return dish.update(updated_dish, dish_id, menu_id, submenu_id)

    @app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=status.HTTP_200_OK)
    def delete_dish(menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID, dish: DishService = Depends()):
        deleted_dish = dish.delete(dish_id, menu_id, submenu_id)
        return deleted_dish

    return app
