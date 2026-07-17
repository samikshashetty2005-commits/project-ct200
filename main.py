from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session as DatabaseSession

from database import Session
from models import Node

app = FastAPI()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "CT200 API is working"
    }


@app.get("/sections")
def get_sections(db: DatabaseSession = Depends(get_db)):

    sections = (
        db.query(Node)
        .filter(Node.parent_id == None)
        .order_by(Node.id)
        .all()
    )

    return sections


@app.get("/node/{node_id}")
def get_node(node_id: int, db: DatabaseSession = Depends(get_db)):

    node = db.query(Node).filter(Node.id == node_id).first()

    if node is None:
        raise HTTPException(
            status_code=404,
            detail="Node not found"
        )

    children = (
        db.query(Node)
        .filter(Node.parent_id == node.id)
        .order_by(Node.id)
        .all()
    )

    return {
        "id": node.id,
        "number": node.number,
        "title": node.title,
        "level": node.level,
        "content": node.content,
        "content_hash": node.content_hash,
        "children": [
            {
                "id": child.id,
                "number": child.number,
                "title": child.title,
                "level": child.level
            }
            for child in children
        ]
    }