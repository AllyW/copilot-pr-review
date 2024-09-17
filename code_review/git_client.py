# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
import json
import os
import requests
import logging
from code_review._exceptions import InvalidGitTokenMissingException, OtherConfigMissingException
from code_review._const import PR_TAG

logger = logging.getLogger(__name__)
PR_COMMENTS_URL_TEMPLATE = "https://api.github.com/repos/{0}/{1}/pulls/{2}/comments"
PR_DIFF_URL_TEMPLATE = "https://api.github.com/repos/{0}/{1}/compare/{2}...{3}"
PR_COMMENT_URL_TEMPLATE = "https://api.github.com/repos/{0}/{1}/pulls/comments/{2}"


class GitClient(object):
    """ git rest api management"""

    def __init__(self):
        self.token = os.environ.get("TOKEN", None)
        if not self.token:
            raise InvalidGitTokenMissingException("GITHUB_TOKEN is required for github rest api")
        self.repository = os.environ.get("REPO", "")
        if not self.repository:
            # AllyW/azure-cli-extensions
            raise OtherConfigMissingException("Please provide pr repository info")
        self.owner, self.repo = self.repository.split("/")

    def get_pr_diff_files(self):
        """
        get https://api.github.com/repos/{owner}/{repo}/compare/{base}...{head}
        :return: 
        """
        raw_event = os.environ.get("EVENT", None)
        if not raw_event:
            raise OtherConfigMissingException("Please provide pr detail info")
        pr_event = json.loads(raw_event)
        pr_request = pr_event["pull_request"]
        base_sha = pr_request["base"]["sha"]
        head_sha = pr_request["head"]["sha"]
        headers = {
            "Accept": "application/vnd.github+json",
            "authorization": f"Bearer {self.token}",
        }

        pr_diff_url = PR_DIFF_URL_TEMPLATE.format(self.owner, self.repo, base_sha, head_sha)

        response = requests.get(pr_diff_url, headers=headers)
        return response.json()

    def comment_pr(self, results: list[dict[str, str]]):
        """
        post https://api.github.com/repos/OWNER/REPO/pulls/{pull_number}/comments
        :param results:
        :return:
        """
        raw_event = os.environ.get("EVENT", None)
        if not raw_event:
            raise OtherConfigMissingException("Please provide pr detail info")
        pr_event = json.loads(raw_event)
        pr_number = pr_event["number"]
        headers = {
            "Accept": "application/vnd.github+json",
            "authorization": f"Bearer {self.token}",
        }
        pr_comment_url = PR_COMMENTS_URL_TEMPLATE.format(self.owner, self.repo, pr_number)
        for item in results:
            requests.post(pr_comment_url, data=json.dumps(item), headers=headers)

    def list_pr_comment(self):
        raw_event = os.environ.get("EVENT", None)
        if not raw_event:
            raise OtherConfigMissingException("Please provide pr detail info")
        pr_event = json.loads(raw_event)
        pr_number = pr_event["number"]
        headers = {
            "Accept": "application/vnd.github+json",
            "authorization": f"Bearer {self.token}",
        }
        pr_comment_url = PR_COMMENTS_URL_TEMPLATE.format(self.owner, self.repo, pr_number)
        response = requests.get(pr_comment_url, headers=headers)
        return response.json()

    def delete_batch_comments(self, comment_ids: list[int]):
        headers = {
            "Accept": "application/vnd.github+json",
            "authorization": f"Bearer {self.token}",
        }
        for comment_id in comment_ids:
            comment_url = PR_COMMENT_URL_TEMPLATE.format(self.owner, self.repo, comment_id)
            res = requests.delete(comment_url, headers=headers)
            logger.warning("Delete comment {0} res: {1}".format(comment_id, res))

    def reset_pr_comment(self):
        pre_comments = self.list_pr_comment()
        deleted_comment_ids: list[int] = []
        for comment in pre_comments:
            logger.warning("Comments detail: {0}".format(comment))
            if comment["body"].find(PR_TAG.strip()) != -1:
                deleted_comment_ids.append(comment["id"])
        logger.warning("Comment is to be deleted: {0}".format(deleted_comment_ids))
        self.delete_batch_comments(deleted_comment_ids)
