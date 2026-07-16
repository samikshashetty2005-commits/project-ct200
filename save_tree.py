from database import Session
from models import Node

import hashlib
def generate_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()



session = Session()
def save_node(tree_node, parent_id=None):
    db_node = Node(
        title=tree_node.title,
        number=tree_node.number,
        level=tree_node.level,
        parent_id=parent_id,
        content=tree_node.content,
        content_hash=generate_hash(tree_node.content)
    )

    session.add(db_node)
    session.commit()
    session.refresh(db_node)
    for child in tree_node.children:
        save_node(child, db_node.id)
from pdf_tree_parser import parse_manual

with open("manual.txt", encoding="utf8") as f:
    text = f.read()

tree = parse_manual("manual.txt")

for child in tree.children:
    save_node(child)

session.close()

print("✅ Tree saved successfully!")