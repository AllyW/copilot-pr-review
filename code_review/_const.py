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

MAX_PATCH_LIMITATION = 8000

PR_SUMMARY_PROMPT = """
Below is the whole changed content from a github pull requests, please draw a summary of this pr with no more than 100 words. Please use the following format:
PR Summary:
1. balabala
2. balabala
...
"""

PR_DIFF_COMP_PROMPT = """
Below is the diff info from a github pull requests, please make a simple code review, and find the places that can be refined, in a simple and concise way. Please describe the refinement with no more than 100 words. And for the return message please follow the following rules:
1. if the code diff is like "VERSION=something", please ignore this change and do not return any review result, just return Review-Ignored;
2. if the code diff is like history notes, please just check the sentence grammar, if no grammar error, please do not return anything; 
3. if the help messages, notes, comments or examples contains '<>', please ensure it's surrounding html tags, if it's not, then please ensure it uses backtick to mark it as placeholder, if not, please pointed it out
4. if the help messages, comments contains url link, please help check whether the url link is accessible, if it's not accessible, please make sure it uses backtick to mark it as an fake url example, if not, pointed it out.
Please pay attention, do not say anything if the diff code follow above rules, nothing like 'Everything else looks good.' needs to be returned, just do not return anything
"""

PR_TAG = """
:mag_right:
"""
