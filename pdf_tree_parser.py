import re
import json

def parse_manual(filename):
    f = open(filename, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()

    root = {
        "id": 0,
        "number": "0",
        "title": "Manual",
        "level": 0,
        "content": "",
        "children": []
    }

    stack = [root]
    node_id = 1

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(r"^(\d+(?:\.\d+)*)\.?\s+(.+)$", line)

        if match:
            num = match.group(1)
            title = match.group(2)
            level = len(num.split('.'))

            new_node = {
                "id": node_id,
                "number": num,
                "title": title,
                "level": level,
                "content": "",
                "children": []
            }
            node_id += 1

            while len(stack) > 1 and stack[-1]["level"] >= level:
                stack.pop()

            stack[-1]["children"].append(new_node)
            stack.append(new_node)
        else:
            current = stack[-1]
            if current["content"] == "":
                current["content"] = line
            else:
                current["content"] += "\n" + line

    return root

data = parse_manual("manual.txt")
print(json.dumps(data, indent=4))