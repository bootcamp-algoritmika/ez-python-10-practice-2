from datetime import datetime
from typing import List

from adapters.interfaces import IssueServiceI
from domain.issue.dto import CreateIssueDTO, UpdateIssueDTO, PartiallyUpdateIssueDTO
from domain.issue.model import Issue
from domain.issue.storage import IssueStorageI


class IssueService(IssueServiceI):
    def __init__(self, storage: IssueStorageI):
        self.storage = storage

    def get_issues(self, limit: int, offset: int) -> List[Issue]:
        # in real life any filters or something else
        issues = self.storage.get_all(limit, offset)
        return issues

    def get_issue(self, issue_id) -> Issue:
        issues = self.storage.get_one(issue_id=issue_id)
        return issues

    def create_issue(self, issue: CreateIssueDTO) -> Issue:
        issue = Issue(**issue.__dict__, created_date=datetime.strftime(datetime.utcnow(), "%s"))
        return self.storage.create(issue=issue)

    def delete_issue(self, issue_id) -> None:
        self.storage.delete(issue_id=issue_id)

    def update_issue(self, issue: UpdateIssueDTO):
        issue = Issue(**issue.__dict__)
        issue.modified_date = datetime.strftime(datetime.utcnow(), "%s")
        self.storage.update(issue=issue)

    def partially_update(self, issue: PartiallyUpdateIssueDTO):
        old_issue = self.get_issue(issue.id)
        if issue.status is not None:
            old_issue.status = issue.status
        if issue.title is not None:
            old_issue.title = issue.title
        if issue.text is not None:
            old_issue.text = issue.text
        if issue.assignee is not None:
            old_issue.assignee = issue.assignee
        if issue.tags is not None and len(issue.tags) > 0:
            old_issue.tags = issue.tags
        if issue.author is not None:
            old_issue.author = issue.author

        old_issue.modified_date = datetime.strftime(datetime.utcnow(), "%s")
        self.storage.update(issue=old_issue)
