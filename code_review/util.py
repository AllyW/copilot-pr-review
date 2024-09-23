# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
import re
import logging
logger = logging.getLogger(__name__)

GIT_PATCH_PATTERN = r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@'


def filter_review_patch_pattern(patch_body: str) -> bool:
    matches = re.findall(GIT_PATCH_PATTERN, patch_body)
    return len(matches) != 1


def get_patch_position(patch_body: str) -> int | None:
    match = re.match(GIT_PATCH_PATTERN, patch_body)
    if match:
        old_start, old_length, new_start, new_length = match.groups()
    else:
        logger.warning("No git patch found, shouldn't be here")
        return
    start: int = int(new_start)
    last_add: int = 0
    line_add: int = 0
    logger.warning("patch body: {0}".format(patch_body))
    logger.warning("start line: {0}".format(start))
    for line in patch_body.split("\n"):
        if line.find("-") == 0:
            continue
        line_add += 1
        if line.find("+") == 0:
            last_add = line_add
    return start + last_add - 2
