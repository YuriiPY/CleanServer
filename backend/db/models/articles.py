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


class Articles(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(Text)
    link: Mapped[str] = mapped_column(Text, nullable=False)
    published_date: Mapped[Date | None] = mapped_column(Date)
    pdf_path: Mapped[str | None] = mapped_column(Text)

    content: Mapped["ArticleContent"] = relationship(
        back_populates="article",
        uselist=False,
        cascade="all, delete-orphan"
    )

    @property
    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "link": self.link,
            "published_date": self.published_date,
            "pdf_path": self.pdf_path
        }
