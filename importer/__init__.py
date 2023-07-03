from .client import ApiClient
from .finder import Finder

class Importer:

    def __init__(self, api_server, token, dir_path, is_publish=True):
        self.api_server = api_server
        self.token = token
        self.dir_path = dir_path

        self.api_server = ApiClient(api_server, token)
        self.is_publish = is_publish

    def run(self):
        self.api_server.auth()
        collections = Finder.scan(self.dir_path)

        for c in collections:
            self._import_collection(c)

    def _import_collection(self, collection):
        print("Create collection: {}".format(collection.name))
        cid = self.api_server.create_collection(collection)

        for doc in collection.documents:
            doc.cid = cid
            self._import_document(doc)

    def _import_document(self, document):
        print("Create document: {}".format(document.title))
        doc_id = self.api_server.create_document(document, self.is_publish)

        if document.has_sub_doc:
            for doc in document.sub_documents:
                doc.cid = document.cid
                doc.pid = doc_id
                self._import_document(doc)
