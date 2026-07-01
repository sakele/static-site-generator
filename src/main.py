import os, shutil
from gencontent import generate_page

def main():
    copy_dir("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")

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