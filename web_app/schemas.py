import uuid
from decimal import Decimal
from pydantic import BaseModel


class MenuRequestCreate(BaseModel):
    title: str = f"menu title"
    description: str = "menu description"

    class Config:
        orm_mode = True


class MenuRequest(MenuRequestCreate):
    id: uuid.UUID
    submenus_count: int = 0
    dishes_count: int = 0


class SubMenuRequestCreate(BaseModel):
    title: str = f"submenu title"
    description: str = "submenu description"

    class Config:
        orm_mode = True


class SubMenuRequest(SubMenuRequestCreate):
    id: uuid.UUID
    dishes_count: int = 0


class DishRequestCreate(BaseModel):
    title: str = f"dish title"
    description: str = "dish description"
    price: Decimal

    class Config:
        orm_mode = True


class DishRequest(DishRequestCreate):
    id: uuid.UUID
