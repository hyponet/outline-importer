# 🔌 outline-importer

## What's Outline

An open, extensible, wiki for your team built using React and Node.js.

- Website: https://www.getoutline.com
- Github: https://github.com/outline/outline

## What's outline-importer

outline-importer is a simple tool to import documents from markdown files.

### Usage

Make sure your **Directory Structure** like this(This directory structure is consistent with the export from Outline)

```
| - wiki_dir
|      | - dir1
|      |    | - doc1.md
|      |    | - doc2.md
|      |
|      | - dir2
|           | - doc3.md
|           | - doc3
|                | - doc4.md
|                | - doc5.md
```

In the above example, Importer will create two collections: dir1 and dir2, 
the document doc4.md、doc5.md will become a sub-document of doc3.

git clone:

```
git clone https://github.com/Coderhypo/outline-importer.git
```

run to import

```
pip install requests
python3 cli.py --server SERVER --token TOKEN --dir DIR_PATH
```

such as:

```
python cli.py --server http://localhost:3000/ --token JmDYPAHAKiGpMB9KJbWkIHkFSfv0RQX5oNpRgh --dir /Users/hypo/outline
```

## Bug report

If you are having trouble using it, please create an issue.😊

## TODO

1. Add tests
2. Use the docker image to handle no python environment