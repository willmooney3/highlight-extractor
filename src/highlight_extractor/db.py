import os
import sqlite3


class SQLiteDatabaseManager(object):
    def __init__(self):
        super().__init__()
        self.path = os.path.join(os.path.expanduser("~"), ".highlight_extractor.db")
        self.connection = sqlite3.connect(self.path)

    def create_database(self) -> None:
        cur = self.connection.cursor()
        cur.execute(
            "".join(
                [
                    "CREATE TABLE IF NOT EXISTS highlights ",
                    "(doc_path text,page integer,img_path text,content text)",
                ]
            )
        )
        cur.close()

    def add_highlight(
        self, doc_path: str, page: int, img_path: str, content: str = ""
    ) -> None:
        cur = self.connection.cursor()
        query = (
            "INSERT INTO highlights (doc_path,page,img_path,content) VALUES (?,?,?,?)"
        )
        cur.execute(query, (doc_path, page, img_path, content))
        cur.close()
