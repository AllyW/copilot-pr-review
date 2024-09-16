# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------


AZURE_MODEL = "gpt-4o"
MODEL_API_VERSION = "2024-02-15-preview"

MODEL_SYSTEM_ROLE = "system"
MODEL_USER_ROLE = "user"
MODEL_ASSIST_ROLE = "assistant"

MAX_PATCH_LIMITATION = 800

PR_SUMMARY_PROMPT = """
Below is the whole changed content from a github pull requests, please draw a summary of this pr with no more than 100 words. Please use the following format:
PR Summary:
1. balabala
2. balabala
...
"""

PR_DIFF_COMP_PROMPT = """
Below is the diff info from a github pull requests, please make a simple code review, and find the places that can be refined, in a simple and concise way. Please describe the refinement with no more than 100 words
"""

PR_TAG = " :mag_right: "
