
from sqlalchemy import Column, Integer, String, Text
from database import Base


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    number = Column(String)

    level = Column(Integer)

    parent_id = Column(Integer)

    content = Column(Text)

    content_hash = Column(String)