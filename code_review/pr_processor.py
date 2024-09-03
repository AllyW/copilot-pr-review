# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
import os
import logging
from code_review.git_client import GitClient
from code_review.gpt_client import GptClient, format_gpt_message
from code_review._const import MAX_PATCH_LIMITATION, PR_DIFF_COMP_PROMPT, PR_SUMMARY_PROMPT, MODEL_USER_ROLE
logger = logging.getLogger(__name__)


class PRProcessor(object):

    def __init__(self):
        self.git_manager = GitClient()
        self.gpt_manager = GptClient()

    def review_pr(self):
        pr_diffs = self.git_manager.get_pr_diff_files()
        code_suggest = os.environ.get("code_suggest", False)
        if code_suggest:
            self.__review_pr_code_line__(pr_diffs)
        pr_summary = os.environ.get("pr_summary", True)
        if pr_summary:
            self.__review_pr_summary__(pr_diffs)

    def __review_pr_code_line__(self, pr_diffs):
        if not pr_diffs or "files" not in pr_diffs or not pr_diffs["files"]:
            logger.warning("No pr diff files, code review ignored")
        commit_id = pr_diffs["commits"][-1]["sha"]
        review_res = []
        for diff_item in pr_diffs["files"]:
            filename = diff_item["filename"]
            patch = diff_item["patch"]
            status = diff_item["status"]
            if status not in ["modified", "added"]:
                continue
            if not patch or len(patch) > MAX_PATCH_LIMITATION:
                logger.warning("file {0} diff exceeds max token limitation".format(filename))
                continue
            messages = []
            format_gpt_message(messages, [PR_DIFF_COMP_PROMPT], role=MODEL_USER_ROLE)
            format_gpt_message(messages, [patch], role=MODEL_USER_ROLE)
            gpt_resp = self.gpt_manager.request_gpt(messages)
            if not gpt_resp:
                continue
            review_item = {
                "file_path": filename,
                "commit_id": commit_id,
                "review_content": gpt_resp,
                "position": len(patch.split("\n")) - 1
            }
            review_res.append(review_item)
        self.git_manager.comment_pr(review_res)

    def __review_pr_summary__(self, pr_diffs):
        if not pr_diffs or "files" not in pr_diffs or not pr_diffs["files"]:
            logger.warning("No pr diff files, pr summary ignored")
        commit_id = pr_diffs["commits"][-1]["sha"]
        pr_contents = [diff_item["patch"] for diff_item in pr_diffs["files"]]
        messages = []
        format_gpt_message(messages, [PR_SUMMARY_PROMPT], role=MODEL_USER_ROLE)
        format_gpt_message(messages, [pr_contents.join("\n")], role=MODEL_USER_ROLE)

        gpt_resp = self.gpt_manager.request_gpt(messages)
        if not gpt_resp:
            return
        review_item = {
            "file_path": pr_diffs["files"][0]["filename"],
            "commit_id": commit_id,
            "review_content": gpt_resp,
            "position": 0
        }
        self.git_manager.comment_pr([review_item])
