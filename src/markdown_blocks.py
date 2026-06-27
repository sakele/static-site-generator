from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = list(map(str.strip, blocks))
    for block in blocks[:]:
        if block.isspace() or block == "":
            blocks.remove(block)
    return blocks

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and block.startswith("```\n") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        html_node = block_to_html_node(block)
        child_nodes.append(html_node)
    return ParentNode("div", child_nodes)

def block_to_html_node(block: str) -> ParentNode:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        if block_type == BlockType.HEADING:
            return heading_to_html_node(block)
        if block_type == BlockType.CODE:
            return code_to_html_node(block)
        if block_type == BlockType.QUOTE:
            return quote_to_html_node(block)
        if block_type == BlockType.OLIST:
            return olist_to_html_node(block)
        if block_type == BlockType.ULIST:
            return ulist_to_html_node(block)

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = list(map(text_node_to_html_node, text_nodes))
    return children

def paragraph_to_html_node(block: str) -> ParentNode:
    paragraph = block.replace('\n', ' ')
    child_nodes = text_to_children(paragraph)
    return ParentNode("p", child_nodes)

def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char =="#":
            level += 1
        else:
            break
    if level > 6:
        raise ValueError(f"invalid heading level: {level}")
    split_text = block.split("# ", maxsplit=1)
    text = split_text[1]
    child_nodes = text_to_children(text)
    return ParentNode(f"h{level}", child_nodes)

def code_to_html_node(block: str) -> ParentNode:
    block_text = block[4:-3]
    text_node = TextNode(block_text, TextType.CODE)
    child_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [child_node])

def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if line.startswith("> "):
            split_text = line.split("> ", maxsplit=1)
        elif line.startswith(">"):
            split_text = line.split(">", maxsplit=1)
        else:
            raise ValueError("invalid quote block")
        new_line = split_text[1]
        new_lines.append(new_line)
    new_text = " ".join(new_lines)
    child_nodes = text_to_children(new_text)
    return ParentNode("blockquote", child_nodes)

def olist_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_nodes = []
    i = 1
    for line in lines:
        split_line = line.split(f"{i}. ", maxsplit=1)
        i += 1
        new_line = split_line[1]
        child_nodes = text_to_children(new_line)
        new_node = ParentNode("li", child_nodes)
        new_nodes.append(new_node)
    return ParentNode("ol", new_nodes)

def ulist_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_nodes = []
    for line in lines:
        split_line = line.split("- ", maxsplit=1)
        new_line = split_line[1]
        child_nodes = text_to_children(new_line)
        new_node = ParentNode("li", child_nodes)
        new_nodes.append(new_node)
    return ParentNode("ul", new_nodes)
