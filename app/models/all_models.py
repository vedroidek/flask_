from decimal import Decimal
import enum
from typing import List, Annotated
from datetime import date
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[intpk]


@enum.unique
class UserStatus(enum.Enum):
    is_root = 'root'
    is_user = 'user'
    is_admin = 'admin'


class User(BaseModel):
    """ User model. """
    def __init__(self, name, password, email):
        self.name: str = name
        self.password: str = password
        self.email: str = email
        
    __tablename__ = 'user'

    name: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    profile: Mapped['UserProfile'] = relationship(back_populates='user')
    order: Mapped[List["Order"]] = relationship()
    
    def __repr__(self):
        return f'User {self.name}'
    
    @property
    def is_authenticated(self):
        return self.is_active
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)


class UserProfile(BaseModel):
    __tablename__ = 'profile'

    second_name: Mapped[str | None] = mapped_column(String(32))
    last_name: Mapped[str | None] = mapped_column(String(64))
    locate: Mapped[str | None] = mapped_column(String(256))
    age: Mapped[int]
    birthdate: Mapped[date | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped['User'] = relationship(back_populates='profile', cascade="all, delete")
    
    
@enum.unique
class TypeOfBill(enum.Enum):    
    CARD = 'Card'
    PAYMENT_ACCOUNT = 'Payment account'
    
    
class UserBill(Base):
    __tablename__ = 'bill'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    type_of_bill: Mapped['TypeOfBill'] = mapped_column(nullable=False, default=TypeOfBill.PAYMENT_ACCOUNT)
    type_card_or_bill: Mapped[str] = mapped_column(String(64), nullable=False)
    owner: Mapped['User'] = mapped_column(ForeignKey('user.id'))
    phone_number: Mapped[str | None] = mapped_column(String(12), unique=True)
    

@enum.unique
class OrderStatus(enum.Enum):
    AWAITING_PAYMENT = 'Awaiting payment'
    PAID = 'Paid'
    ANNULLED = 'Annulled'

    
class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    total_cost: Mapped[Decimal]
    user_id: Mapped['User'] = mapped_column(ForeignKey('user.id'), name='requisites')
    status: Mapped['OrderStatus'] = mapped_column(nullable=False, default=OrderStatus.AWAITING_PAYMENT)
