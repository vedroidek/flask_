from decimal import Decimal
import enum
from typing import List, Annotated
from datetime import date
from sqlalchemy import String, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db


intpk = Annotated[int, mapped_column(primary_key=True)]


class BaseUserModel(db.Model):
    __abstract__ = True

    id: Mapped[intpk]


@enum.unique
class UserStatus(enum.Enum):
    is_root = 'root'
    is_user = 'user'
    is_admin = 'admin'


class User(BaseUserModel):
    __tablename__ = 'user'

    name: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    profile: Mapped['UserProfile'] = relationship(back_populates='user')
    order: Mapped[List["Order"]] = relationship()
    
    def __repr__(self):
        return f'User {self.name}'


class UserProfile(BaseUserModel):
    __tablename__ = 'profile'

    second_name: Mapped[str | None] = mapped_column(String(32))
    last_name: Mapped[str | None] = mapped_column(String(64))
    locate: Mapped[str | None] = mapped_column(String(256))
    phone_number: Mapped[str | None] = mapped_column(String(12), unique=True)
    age: Mapped[int]
    birthdate: Mapped[date | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped['User'] = relationship(back_populates='profile', cascade="all, delete")
    
    
class UserRequisites():
    pass


@enum.unique
class OrderStatus(enum.Enum):
    AWAITING_PAYMENT = 'Awaiting payment'
    PAID = 'Paid'
    ANNULLED = 'Annulled'


def get_user_limit(id):
    limit = None
    # here the user's card limit is requested
    return limit
    

class Order(db.Model):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    total_cost: Mapped[Decimal]
    user_id: Mapped['User'] = mapped_column(ForeignKey('user.id'), name='requisites')
    status: Mapped['OrderStatus'] = mapped_column(nullable=False, default=OrderStatus.AWAITING_PAYMENT)
