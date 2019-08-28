import os


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

    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.collections = []
        self.orphans = []

    def scan(self):
        files = os.listdir(self.dir_path)
        for file in files:
            curt_path = "{}/{}".format(self.dir_path, file)
            if os.path.isdir(curt_path):
                self.collections.append(Collection(
                    path=curt_path,
                    name=file,
                ))
            else:
                if not (file.endswith(".md") or file.endswith(".MD")):
                    print("{} is not a markdown file".format(curt_path))
                    continue
                file = file.replace(".md", "")
                file = file.replace(".MD", "")
                self.orphans.append(Document(
                    path=curt_path,
                    title=file,
                ))

        for c in self.collections:
            self._fill_collection(c)

        if self.orphans:
            uncategorized = Collection("", "uncategorized")
            uncategorized.documents += self.orphans
            self.collections.append(uncategorized)
        return self.collections

    def _fill_collection(self, collection):
        files = os.listdir(collection.path)
        for file in files:
            curt_path = "{}/{}".format(collection.path, file)
            doc = Document(curt_path, file)

            if os.path.isdir(curt_path):
                if os.path.isfile(curt_path + ".md") or os.path.isfile(curt_path + ".MD"):
                    continue
                doc.has_sub_doc = True
            else:
                if not (file.endswith(".md") or file.endswith(".MD")):
                    print("{} is not a markdown file".format(curt_path))
                    continue
                doc.title = doc.title.replace(".md", "")
                doc.title = doc.title.replace(".MD", "")

                sub_path = "{}/{}".format(collection.path, doc.title)
                if os.path.isdir(sub_path):
                    doc.has_sub_doc = True
                    doc.sub_path = sub_path

            if doc.has_sub_doc:
                self._fill_document(doc)
            collection.documents.append(doc)

    def _fill_document(self, document):
        if not document.has_sub_doc:
            return

        files = os.listdir(document.sub_path)
        for file in files:
            curt_path = "{}/{}".format(document.sub_path, file)
            doc = Document(curt_path, file)

            if os.path.isdir(curt_path):
                if os.path.isfile(curt_path + ".md") or os.path.isfile(curt_path + ".MD"):
                    continue
                doc.has_sub_doc = True
                doc.sub_path = curt_path
            else:
                if not (file.endswith(".md") or file.endswith(".MD")):
                    print("{} is not a markdown file".format(curt_path))
                    continue
                doc.title = doc.title.replace(".md", "")
                doc.title = doc.title.replace(".MD", "")
                sub_path = "{}/{}".format(document.sub_path, doc.title)
                if os.path.isdir(sub_path):
                    doc.has_sub_doc = True
                    doc.sub_path = sub_path

            if doc.has_sub_doc:
                self._fill_document(doc)
            document.sub_documents.append(doc)
