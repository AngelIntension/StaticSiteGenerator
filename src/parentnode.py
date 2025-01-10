from functools import reduce
from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children):
        super().__init__(tag, None, children)

    def to_html(self):
        if self.tag is None:
            raise ValueError("parent node must have a tag")
        if self.children is None:
            raise ValueError("parent node must have a child")
        inner_text = ''.join(list(reduce(lambda acc, node: acc + node.to_html(), self.children, "")))
        return f"<{self.tag}>{inner_text}</{self.tag}>"
