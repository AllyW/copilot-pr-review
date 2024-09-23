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
Below is the whole changed content from a github pull requests, please draw a summary of this pr with no more than 100 words. Ignore the history notes updates. 
And please use the following format:
PR Summary:
1. balabala
2. balabala
...
"""

PR_DIFF_COMP_PROMPT = """
Below is the diff info from a github pull requests, please make a simple code review, and find the places that can be refined, in a simple and concise way. Please describe the refinement with no more than 100 words. And for the return message please follow the following rules:
1. if the code diff is like "VERSION=something", please ignore review this code change and do not return anything, just do not return anything;
2. if the code diff is from history notes, help messages or examples, please just check the sentence grammar, if no grammar error, please do not return anything; 
3. if the code diff is from history notes, help messages or examples, and contains '<>', please ensure it's surrounding html tags, if it's not, then please ensure it uses backtick to mark it as placeholder, if not, please pointed it out. If they contains url link, please help check whether the url link is accessible, if it's not accessible, please make sure it uses backtick to mark it as an fake url example, if not, pointed it out. Please pay attention, for history notes, help messages or examples, do not say anything if they follow previous rules, nothing like 'Everything else looks good.' needs to be returned, just do not return anything
4. for code diff from python, please review it as an expert python programmer, give a refined way for it if applicable. If your advice is just a different way for writing it, then please do not return anything. Just give the review suggestion that you thnk is way more refined, and git it in a concise manner.
5. please only review the code line start with '-' and '+', as they are the git code diff line, other lines do not need to be reviewed.
"""

PR_TAG = """
:mag_right:
"""

PR_EVALUATE_SYSTEM_SET = """
You are an expert in github pr developer and reviewer.
"""


PR_EVALUATE_PROMPT = """
Below is a list of evaluation score for existing git pr review result and its corresponding score, delimitd by @@@.
Nothing to return.@@@-10
The URL is incomplete. It should be https://learn.microsoft.com/en-us/cli/azure/monitor/data-collection/endpoint/association?view=azure-cli-latest#az-monitor-data-collection-endpoint-association-list.@@@5
The placeholder <resource/monitor/endpoint_id> should be enclosed in backticks for clarity and compliance with markdown formatting.@@@3
`az aks connection create` should be backticked in the history notes for consistency with the previous usage.@@@-1
Review-Ignored@@@-10
Can you evaluate the below sentence according to the standard set up in the above evaluation example data list, just give a score please:

"""

DEFAULT_EVALUATE_SCORE = -1
