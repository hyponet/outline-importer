import os
import random

import requests
from requests import Session

from requests.packages import urllib3

# diable warn log for self-sign cert
urllib3.disable_warnings()


class HttpClient(Session):

    def __init__(self, base_url, token):
        super(HttpClient, self).__init__()
        self.base_url = base_url
        self.token = token
        self.verify = False
        self.headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Encoding': ', '.join(('gzip', 'deflate')),
            'Connection': 'keep-alive',
        }

    def __url(self, path):
        return "{}{}".format(self.base_url, path)

    def post(self, path, data=None, json=None, **kwargs):
        return super(HttpClient, self).post(self.__url(path), data=data, json=json, **kwargs)

    def get(self, path, **kwargs):
        return super(HttpClient, self).get(self.__url(path), **kwargs)

    def try_auth(self):
        rsp = self.get("/api/auth.info", params={"token": self.token})
        return rsp.status_code // 100 == 2

    def create_collection(self, name, desc):
        color = "0123456789ABCDEF"
        data = {
            "name": name,
            "description": desc,
            "color": "#" + "".join(random.sample(color, 6)),
        }
        rsp = self.post("/api/collections.create", json=data)
        try:
            if rsp.status_code // 100 != 2:
                raise RuntimeError(rsp.json())
            collection = rsp.json()
        except requests.JSONDecodeError as err:
            print("decode failed load json content: status={} body={}".format(rsp.status_code, rsp.text))
            raise err
        return collection['data']['id']

    def create_document(self, cid, pid, title, text, is_publish):
        data = {
            "collectionId": cid,
            "parentDocumentId": pid,
            "publish": is_publish,
            "text": text,
            "title": title,
        }
        rsp = self.post("/api/documents.create", json=data)
        if rsp.status_code // 100 != 2:
            raise RuntimeError(rsp.json())
        document = rsp.json()
        return document['data']['id']


class ApiClient:
    def __init__(self, api_server, token):
        self.api_server = api_server
        self.http_client = HttpClient(api_server, token)

    def auth(self):
        if self.http_client.try_auth():
            return
        raise RuntimeError(
            "Authentication failed. "
            "ApiServer: {}".format(self.api_server))

    def create_collection(self, collection):
        return self.http_client.create_collection(
            name=collection.name,
            desc=collection.description,
        )

    def create_document(self, document, is_publish):
        if os.path.isfile(document.path):
            with open(document.path, encoding="utf8") as f:
                text = f.read()
        else:
            text = "# {}".format(document.title)

        return self.http_client.create_document(
            cid=document.cid,
            pid=document.pid,
            title=document.title,
            text=text,
            is_publish=is_publish,
        )
