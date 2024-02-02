from decimal import Decimal
import enum
from datetime import datetime
from typing import Annotated
from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]


class BaseUserModel(db.Model):
    __abstract__ = True

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[created_at]


@enum.unique
class UserStatus(enum.Enum):
    user = 'user'
    admin = 'admin'


class User(BaseUserModel):
    __tablename__ = 'users'

    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    profile: Mapped["UserProfile"] = relationship(back_populates="user",
                                                  cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'User "{self.name}"'
    
    @classmethod
    def get_user_limit(self):
        limit = None
        # here the user's card limit is requested
        return limit


class UserProfile(BaseUserModel):
    __tablename__ = 'profile'

    second_name: Mapped[str | None] = mapped_column(String(32))
    last_name: Mapped[str | None] = mapped_column(String(64))
    locate: Mapped[str | None] = mapped_column(String(256))
    phone_number: Mapped[str | None] = mapped_column(String(12), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates="profile")
    
    
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

    id: Mapped[intpk]
    limit: Mapped[Decimal] = mapped_column(get_user_limit(User.id))
    requisites: Mapped['User'] = mapped_column(ForeignKey('users.id'))
    user_id: Mapped[int] = relationship(back_populates='order')
    status: Mapped['OrderStatus'] = mapped_column(nullable=False, default=OrderStatus.AWAITING_PAYMENT,)
