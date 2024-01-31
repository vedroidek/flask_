import enum
from datetime import datetime
from typing import Annotated
from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from app.models.user import intpk, created_at, User, UserProfile


class Order(db.Model):
    __tablename__ = 'payments'

    id: Mapped[intpk]
    created_at: Mapped[created_at]
    profile_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))