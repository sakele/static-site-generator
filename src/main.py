import os, shutil
from textnode import TextNode, TextType

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")
    print(text_node)
    copy_dir("./static", "./public")

def copy_dir(source, destination):
    if not os.path.exists(source):
        raise Exception("path to source directory does not exist")
    if os.path.exists(destination):
        print(f"REMOVING DIRECTORY: {destination}")
        shutil.rmtree(destination)
    os.mkdir(destination)
    items = os.listdir(source)
    for item in items:
        source_subpath = os.path.join(source, item)
        destination_subpath = os.path.join(destination, item)
        if os.path.isfile(source_subpath):
            print(f"COPYING ITEM: {source_subpath} to {destination_subpath}")
            shutil.copy(source_subpath, destination)
        else:
            copy_dir(source_subpath, destination_subpath)
        
    

main()