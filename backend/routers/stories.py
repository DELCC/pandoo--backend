from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import StoryRead, StoryCreate
from models import  Product, Child, Story
from db.database import get_db


router = APIRouter(prefix='/stories',  tags=["Stories"])

@router.post("/",response_model = StoryRead)
def add_products(id_child : int, new_story : StoryCreate ,db : Session = Depends(get_db)):
    child = db.query(Child).filter(id_child == Child.id).first()

    if not child:
        raise HTTPException(
            status_code=404,
            detail="Child not found"
        )

    new_story = Story(
        id=new_story.id,
        url_mp3=new_story.url_mp3,
        script=new_story.script,
        id_child = child.id)
    
    db.add(new_story)
    db.commit()
    db.refresh(new_story)

    return new_story