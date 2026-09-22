from uuid import UUID, uuid4
from sqlalchemy import String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
from datetime import datetime

class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(nullable=True)
    action: Mapped[str] = mapped_column(String, index=True)
    resource: Mapped[str] = mapped_column(String)
    payload: Mapped[dict] = mapped_column(JSON)
    ip_address: Mapped[str] = mapped_column(String)
    severity: Mapped[str] = mapped_column(String, default="INFO")
