from fastapi import FastAPI,Depends,status,Response
from . import models,shema
from sqlalchemy.orm import session

from .database import engine,SessionLocal


models.Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/blog")
def Blog(db:session=Depends(get_db)):
    blogs=db.query(models.Blog).all()

    return blogs


@app.get("/blog/{id}")
def get_blog(id,db:session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    return blog


@app.post("/blog",status_code=status.HTTP_201_CREATED)
def create_blog(request:shema.Blog,db:session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return{"data":new_blog}