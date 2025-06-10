from datetime import datetime
from sqlalchemy import ForeignKey, func, Text
from sqlalchemy.orm import Mapped, mapped_column, registry
from datetime import datetime


table_registry = registry()


@table_registry.mapped_as_dataclass
class UserModel:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    username: Mapped[str] = mapped_column(
        unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(
        nullable=False, unique=True
    )
    avatar_url: Mapped[str] = mapped_column(nullable=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey('roles.id'), nullable=False
    )


@table_registry.mapped_as_dataclass
class RolesModel:
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(
        unique=True, nullable=False
    )
    level: Mapped[int] = mapped_column(nullable=False)


@table_registry.mapped_as_dataclass
class DonorModel:
    __tablename__ = 'donors'
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    name: Mapped[str] = mapped_column(nullable=False)
    avatar_url: Mapped[str] = mapped_column(nullable=True)
    cpf_cnpj: Mapped[str] = mapped_column(
        nullable=False, unique=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )


@table_registry.mapped_as_dataclass
class InstitutionModel:
    __tablename__ = 'institutions'
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    name: Mapped[str] = mapped_column(nullable=False)
    sector: Mapped[str] = mapped_column(nullable=False)
    avatar_url: Mapped[str] = mapped_column(nullable=True)
    cnpj: Mapped[str] = mapped_column(
        nullable=False, unique=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )


@table_registry.mapped_as_dataclass
class DonationModel:
    __tablename__ = 'donations'
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    amount: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), init=False
    )
    payment_method: Mapped[str] = mapped_column(
        nullable=False
    )
    donor_id: Mapped[int] = mapped_column(
        ForeignKey('donors.id'), nullable=False
    )
    institution_id: Mapped[int] = mapped_column(
        ForeignKey('institutions.id'), nullable=False
    )
