# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
import json
import os
import logging
from typing import Any
from code_review.git_client import GitClient
from code_review.gpt_client import GptClient, format_gpt_message
from code_review.util import filter_review_patch_pattern, get_patch_position
from code_review._const import MAX_PATCH_LIMITATION, PR_DIFF_COMP_PROMPT, PR_SUMMARY_PROMPT, MODEL_USER_ROLE, PR_TAG
logger = logging.getLogger(__name__)


class PRProcessor(object):

    def __init__(self):
        self.git_manager = GitClient()
        self.gpt_manager = GptClient()

    def review_pr(self):
        pr_comment_reset = os.environ.get("pr_reset", True)
        if pr_comment_reset:
            self.git_manager.reset_pr_comment()
        pr_diffs = self.git_manager.get_pr_diff_files()
        code_suggest = os.environ.get("code_suggest", False)
        if code_suggest:
            self.__review_pr_code_line__(pr_diffs)
        pr_summary = os.environ.get("pr_summary", True)
        if pr_summary:
            self.__review_pr_summary__(pr_diffs)

    def __review_pr_code_line__(self, pr_diffs: dict[str, Any]) -> None:
        if not pr_diffs or "files" not in pr_diffs or not pr_diffs["files"]:
            logger.warning("No pr diff files, code review ignored")
        commit_id = pr_diffs["commits"][-1]["sha"]
        review_res = []
        for diff_item in pr_diffs["files"]:
            filename = diff_item["filename"]
            patch = diff_item.get("patch", "")
            if filter_review_patch_pattern(patch):
                logger.info("Patch filtered in {0}".format(filename))
                continue
            status = diff_item.get("status", "")
            if status not in ["modified", "added"]:
                continue
            if not patch or len(patch) > MAX_PATCH_LIMITATION:
                logger.warning("file {0} diff exceeds max token limitation".format(filename))
                continue
            messages: list[dict[str, str]] = []
            format_gpt_message(messages, [PR_DIFF_COMP_PROMPT], role=MODEL_USER_ROLE)
            format_gpt_message(messages, [patch], role=MODEL_USER_ROLE)
            gpt_resp = self.gpt_manager.request_gpt(messages)
            if not gpt_resp:
                continue
            review_item = {
                "path": filename,
                "commit_id": commit_id,
                "body": PR_TAG + gpt_resp,
                # "position": len(patch.split("\n")) - 1,
                "start_side": "RIGHT",
                "side": "RIGHT",
                "line": get_patch_position(patch),
                # "start_line": 10,
            }
            logger.warning("code review_item: {0}".format(json.dumps(review_item)))
            review_res.append(review_item)
        self.git_manager.comment_pr(review_res)

    def __review_pr_summary__(self, pr_diffs: dict[str, Any]) -> None:
        if not pr_diffs or "files" not in pr_diffs or not pr_diffs["files"]:
            logger.warning("No pr diff files, pr summary ignored")
        commit_id = pr_diffs["commits"][-1]["sha"]
        pr_contents = [diff_item["patch"] for diff_item in pr_diffs["files"]]
        messages: list[dict[str, str]] = []
        format_gpt_message(messages, [PR_SUMMARY_PROMPT], role=MODEL_USER_ROLE)
        format_gpt_message(messages, ["\n".join(pr_contents)], role=MODEL_USER_ROLE)

        gpt_resp = self.gpt_manager.request_gpt(messages)
        if not gpt_resp:
            return
        review_item = {
            "path": pr_diffs["files"][0]["filename"],
            "commit_id": commit_id,
            "body": PR_TAG + gpt_resp,
            "start_side": "RIGHT",
            "side": "RIGHT",
            "line": 0,
            # "start_line": 10,
        }
        logger.warning("summary review_item: {0}".format(json.dumps(review_item)))
        self.git_manager.comment_pr([review_item])
