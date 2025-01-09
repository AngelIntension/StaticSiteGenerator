class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
        
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        return ' '.join(list(map(lambda kvp: f"{kvp[0]}=\"{kvp[1]}\"", self.props.items())))
