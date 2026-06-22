class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None
    ) -> None:
        
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self) -> str:
        string = ""
        for prop in self.props:
            string += f' {prop}="{self.props[prop]}"'
        return string
    
            
class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None
    ) -> None:
        
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if not self.value:
            raise ValueError("invalid HTML: no value")
        if not self.tag:
            return self.value
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
        html = f"<{self.tag}" + self.props_to_html() + f">{self.value}</{self.tag}>"
        return html
