def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = list(map(str.strip, blocks))
    for block in blocks[:]:
        if block.isspace() or block == "":
            blocks.remove(block)
    return blocks