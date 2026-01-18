from sqlalchemy import and_
from db.session import SessionLocal
from db.models.articles import Articles
from db.models.article_content import ArticleContent


def save_article(article, paragraphs_text, pdf_path):
    with SessionLocal() as session:

        existing_article = session.query(Articles).filter(
            and_(
                Articles.title == article.get("title"),
                Articles.author == article.get("author"),
                Articles.published_date == article.get("date"),
            )
        ).first()

        if existing_article:
            dict_article = existing_article.as_dict
            dict_article["content"] = existing_article.content
            return {"article": dict_article, "exist_status": True}

        db_article = Articles(
            title=article.get("title"),
            author=article.get("author"),
            link=article.get("link"),
            published_date=article.get("date"),
            pdf_path=pdf_path
        )
        session.add(db_article)
        session.flush()

        db_article_text = ArticleContent(
            article_id=db_article.id,
            content=paragraphs_text
        )

        session.add(db_article_text)
        session.commit()

        dict_article = db_article.as_dict
        dict_article["content"] = db_article_text.content

        return {"article": dict_article, "exist_status": False}
