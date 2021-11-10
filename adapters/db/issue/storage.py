from datetime import datetime
from enum import Enum

from domain.issue.exceptions import IssueNotFoundException
from domain.issue.model import Issue
from domain.issue.storage import IssueStorageI


class IssueStatus(Enum):
    NEW = 1
    TO_APPROVE = 2
    APPROVED = 3
    DECLINED = 4


issues_data = {
    '1': Issue(id=1, status=IssueStatus.NEW.value, created_date=datetime.strftime(datetime.utcnow(), "%s"),
               modified_date=datetime.strftime(datetime.utcnow(), "%s"), title="titleA", text="this is textA",
               assignee="someoneA", tags=["a1", "b1", "c1"], author="me"),
    '2': Issue(id=2, status=IssueStatus.APPROVED.value, created_date=datetime.strftime(datetime.utcnow(), "%s"),
               modified_date=datetime.strftime(datetime.utcnow(), "%s"), title="titleB", text="this is textB",
               assignee="someoneB", tags=["a2", "b2", "c2"], author="me"),
    '3': Issue(id=3, status=IssueStatus.NEW.value, created_date=datetime.strftime(datetime.utcnow(), "%s"),
               modified_date=datetime.strftime(datetime.utcnow(), "%s"), title="titleC", text="this is textC",
               assignee="someoneC", tags=["a3", "b3", "c3"], author="me"),
    '4': Issue(id=4, status=IssueStatus.TO_APPROVE.value, created_date=datetime.strftime(datetime.utcnow(), "%s"),
               modified_date=datetime.strftime(datetime.utcnow(), "%s"), title="titleD", text="this is textD",
               assignee="someoneD", tags=["a4", "b4", "c4"], author="me"),
    '5': Issue(id=5, status=IssueStatus.DECLINED.value, created_date=datetime.strftime(datetime.utcnow(), "%s"),
               modified_date=datetime.strftime(datetime.utcnow(), "%s"), title="titleE", text="this is textE",
               assignee="someoneE", tags=["a5", "b5", "c5"], author="me")
}


class IssueStorage(IssueStorageI):

    def create(self, issue: Issue):
        new_issue_id = len(issues_data.keys()) + 1
        issues_data[str(new_issue_id)] = issue
        issue.id = new_issue_id
        return issue

    def update(self, issue: Issue):
        if str(issue.id) not in issues_data.keys():
            raise IssueNotFoundException(message="issue not found")
        issues_data.update({str(issue.id): issue})
        return issue

    def delete(self, issue_id: int):
        try:
            issues_data.pop(str(issue_id))
        except KeyError as e:
            raise IssueNotFoundException(message="issue not found")

    def get_one(self, issue_id: str):
        try:
            return issues_data[str(issue_id)]
        except KeyError as e:
            raise IssueNotFoundException(message="issue not found")

    def get_all(self, limit: int, offset: int):
        issues = list(issues_data.values())[offset:limit + offset]
        return issues
