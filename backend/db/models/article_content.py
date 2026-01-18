from sqlalchemy import (
    String,
    Text,
    Date,
    ForeignKey
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

from db.session import Base


class ArticleContent(Base):
    __tablename__ = "article_content"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    article: Mapped["Articles"] = relationship(
        back_populates="content"
    )
