import argparse
from importer import Importer


class Cli:

    def __init__(self):
        parser = argparse.ArgumentParser(description='Import markdown file to Outline.')
        parser.add_argument('--server', required=True,
                            help='Outline server url, like: http://localhost:3000')
        parser.add_argument('--token', required=True,
                            help='Outline api token')
        parser.add_argument('--dir', required=True,
                            help='markdown file dir')

        self.parser = parser

    def run(self):
        args = self.parser.parse_args()
        server = args.server
        token = args.token
        dir_path = args.dir
        if server.endswith("/"):
            server = server[:-1]
        if dir_path.endswith("/"):
            dir_path = dir_path[:-1]

        importer = Importer(
            api_server=server,
            token=token,
            dir_path=dir_path,
        )
        importer.run()


if __name__ == "__main__":
    cli = Cli()
    cli.run()
