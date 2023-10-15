from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, types
from project.database import Base
from typing import List, Optional
import uuid
import decimal


class Menu(Base):
    __tablename__ = "menus"
    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)
    submenus: Mapped[List["SubMenu"]] = relationship(back_populates="menu")

    def __repr__(self) -> str:
        return f"Menu (id={self.id!r}, title={self.title!r}, description = {self.description!r})"


class SubMenu(Base):
    __tablename__ = "submenus"
    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    description: Mapped[Optional[str]]
    menu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("menus.id", onupdate="CASCADE", ondelete="CASCADE"))
    menu: Mapped[Menu] = relationship(back_populates="submenus")
    dishes: Mapped[List["Dish"]] = relationship(back_populates="submenu", cascade="all,delete")

    def __repr__(self) -> str:
        return f"SubMenu (id={self.id!r}, title={self.title!r}, description = {self.description!r})"


class Dish(Base):
    __tablename__ = "dishes"
    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    description: Mapped[Optional[str]]
    price: Mapped[decimal.Decimal] = mapped_column(types.Numeric(10, 2))
    submenu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("submenus.id", onupdate="CASCADE", ondelete="CASCADE"))
    submenu: Mapped[SubMenu] = relationship(back_populates="dishes")

    def __repr__(self) -> str:
        return f"Dish (id={self.id!r}, title={self.title!r}, description = {self.description!r}), price = {self.price!r}"
