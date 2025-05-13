from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .database import Base


class IdentityCard(Base):

    __tablename__ = "turkish_identity_cards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    identity_number: Mapped[str] = mapped_column(
        String(11), unique=True, nullable=False
    )
    surname: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
