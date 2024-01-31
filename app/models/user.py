import enum
from datetime import datetime
from typing import Annotated
from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
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
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    # status: Mapped[UserStatus] = mapped_column(nullable=False, default=UserStatus.user)

    def __repr__(self):
        return f'User "{self.name}"'


class UserProfile(BaseUserModel):
    __tablename__ = 'profile'

    second_name: Mapped[str | None] = mapped_column(String(32))
    last_name: Mapped[str | None] = mapped_column(String(64))
    locate: Mapped[str | None] = mapped_column(String(256))
    phone_number: Mapped[str | None] = mapped_column(String(12), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
