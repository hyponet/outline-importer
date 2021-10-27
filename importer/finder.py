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
        return Finder.fill_collection(path,Collection("", "uncategorized"))

    @staticmethod
    def fill_collection(path, collection):
        results = []

        for root, subdirs, files in os.walk(path):

            if root != path:
                return results

            for file in [f for f in files if re.search(r"\.md$", f)]:
                file_path = "{}/{}".format(path, file)
                d = Document(file_path, file)
                collection.documents.append(d)
                results.append(collection)

            for dir in subdirs:
                dir_path = "{}/{}".format(path, dir)
                results.append(Finder.fill_collection(dir_path, Collection(dir_path, dir)))

        return collection


