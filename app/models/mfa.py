from uuid import UUID, uuid4
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class MFAModel(Base, TimestampMixin):
    __tablename__ = "mfa"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    secret: Mapped[str] = mapped_column(String)  # Encrypted TOTP secret
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
