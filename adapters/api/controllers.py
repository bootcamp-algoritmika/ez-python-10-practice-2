import json

import falcon

from adapters.interfaces import IssueServiceI
from domain.issue.dto import UpdateIssueDTO, PartiallyUpdateIssueDTO, CreateIssueDTO
from domain.issue.exceptions import IssueNotFoundException


class IssueResource:
    def __init__(self, service: IssueServiceI):
        self.service = service

    def on_get(self, req, resp, issue_id):
        try:
            issue = self.service.get_issue(issue_id=issue_id)
        except IssueNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.body = json.dumps(issue.__dict__)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, issue_id):
        updated_issue = req.media
        if "id" not in updated_issue:
            updated_issue["id"] = issue_id
        dto = UpdateIssueDTO(**updated_issue)
        try:
            self.service.update_issue(dto)
        except IssueNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    def on_patch(self, req, resp, issue_id):
        patched_issue = req.media
        if "id" not in patched_issue:
            patched_issue["id"] = issue_id
        dto = PartiallyUpdateIssueDTO(**patched_issue)
        try:
            self.service.partially_update(dto)
        except IssueNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    def on_delete(self, req, resp, issue_id):
        try:
            self.service.delete_issue(issue_id)
        except IssueNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204


class IssuesResource:
    def __init__(self, service: IssueServiceI):
        self.service = service

    def on_get(self, req, resp):
        limit = req.get_param_as_int('limit') or 50
        offset = req.get_param_as_int('offset') or 0
        issues = self.service.get_issues(limit=limit, offset=offset)
        # или сериализация с помощью pydantic/marshmallow
        # pydantic - быстрее и интерфейс попроще
        res = []
        for u in issues:
            res.append(u.__dict__)
        resp.body = json.dumps(res)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        data = req.get_media()
        new_issue = CreateIssueDTO(**data)
        issue = self.service.create_issue(new_issue)
        resp.status = falcon.HTTP_201
        resp.location = f'/issues/{issue.id}'
