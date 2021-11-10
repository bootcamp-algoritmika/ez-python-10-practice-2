from typing import List


class Issue:
    def __init__(self, status: int, title: str, text: str, assignee: str, tags: List[str], author: str,
                 created_date: str, modified_date: str = None, id: int = None):
        self.id: int = id
        self.status: int = status
        self.title: str = title
        self.text: str = text
        self.assignee: str = assignee
        self.tags: List[str] = tags
        self.author: str = author
        self.created_date: str = created_date
        self.modified_date: str = modified_date
