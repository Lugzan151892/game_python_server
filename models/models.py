from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import DateTime, String, BLOB
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
class Users(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    spectated_users: Mapped[str] = mapped_column(BLOB, nullable=False)
    hunt_settings: Mapped[str] = mapped_column(BLOB, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_onupdate=func.now(), default=func.now())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, created_at=({self.created_at!r}))"


