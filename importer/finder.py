import os
import re

class Collection:

    def __init__(self, path, name, description=None):
        self.name = name
        self.description = description or ""

        self.path = path
        self.documents = []


class Document:
    def __init__(self, path, title):
        self.title = title

        self.path = path
        self.has_sub_doc = False
        self.sub_path = None
        self.sub_documents = []

        self.pid = None
        self.cid = None


class Finder:

    @staticmethod
    def scan(path):
        collections = []

        for dir_name, _, files in os.walk(path):
            collection = Collection(path, dir_name)

            for file in [f for f in files if re.search(r"\.md$", f)]:
                d = Document(f"{path}/{file}", file)
                collection.documents.append(d)

            collections.append(collection)

        return collections
