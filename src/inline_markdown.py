from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif node.text.count(delimiter) % 2 != 0:
            raise ValueError("invalid markdown: formatted section not closed")
        else:
            new_text = node.text.split(delimiter)
            for i in range(len(new_text)):
                if new_text[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(new_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(new_text[i], text_type))
    return new_nodes