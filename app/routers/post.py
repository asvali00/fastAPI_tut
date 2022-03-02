from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# We are retrievning data so we need get method - koristeći ORM
# Sa "db: Session = Depends(get_db)" uspostavljamo konekciju sa bazom podataka i preko toga si omoućavama izvršavanje upita iz pythona
# @router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user.email)
    # kao da ubacio print(post.dict()) - uglavnom dereferencirao si sadžaj koji se nalati na adresi post.dict()
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()  # you always have to commit when you add sth to database
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostVoteResponse)  # SQLALCHEMY
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # sada nećemo tražiti sve nego ćemo filtrirati samo onaj id koji user traži (filter() je ekivivalent SQL WHERE) - i sa posljednjom metodom izvršimo naredbu, prije smo koristili all(), a ona i kada nadje traženi id i dalje će iza nastaviti tražiti, pa je bolje da korstimo first() koji kada nadje jednog završi
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to preform requested action")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    queried_post = db.query(models.Post).filter(models.Post.id == id)
    if queried_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    if queried_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to preform requested action")
    queried_post.delete(synchronize_session=False)
    db.commit()  # remember every time you have changes in database you gotta commit
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    queried_post = db.query(models.Post).filter(models.Post.id == id)
    check_if_post_exist = queried_post.first()
    if check_if_post_exist == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    if queried_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to preform requested action")
    # queried_post.update({'title': 'Hey this is my hardcoded updated content', 'content': 'This is my updated hardcoded content'}, synchronize_session=False) - ovako izgleda kada to hardcodaš
    queried_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return queried_post.first()
