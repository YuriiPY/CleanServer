from fastapi import FastAPI, Depends
import uvicorn
from sqlalchemy.orm import Session
from db.session import SessionLocal, engine
from db.models import Hello

app = FastAPI()


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if "Hello world" already exists
        exists = db.query(Hello).first()
        if not exists:
            hello = Hello(text="Hello world")
            db.add(hello)
            db.commit()
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    except:
        db.close()

@app.get("/")
def read_root(db:Session = Depends(get_db)):

    item = db.query(Hello).first()

    if not item:
        return "None"
    
    return item.text 


if __name__ == "__main__":
    app.add_event_handler("startup", init_db)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)