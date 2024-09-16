# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

import os
import json
import logging
from typing import Optional

from openai import AzureOpenAI
from code_review._const import AZURE_MODEL, MODEL_API_VERSION, MODEL_USER_ROLE
from code_review._exceptions import InvalidOpenAIConfigException
logger = logging.getLogger(__name__)


def format_gpt_message(messages: list[dict[str, str]], contents: list[str], role: str = MODEL_USER_ROLE) -> None:
    """
    fill request messages
    :param messages: messages altered for gpt review
    :param role: message role
    :param contents: message to be reviewed
    :return: None
    """
    for content in contents:
        messages.append({
            "role": role,
            "content": content
        })


class GptClient(object):
    """Gpt client"""

    def __init__(self):
        self.model = os.environ.get("model", AZURE_MODEL)
        self.api_version = os.environ.get("api_version", MODEL_API_VERSION)
        self.azure_endpoint = os.environ.get("ENDPOINT", None)
        self.azure_api_key = os.environ.get("APIKEY", None)
        if not self.azure_endpoint or not self.azure_api_key:
            raise InvalidOpenAIConfigException("Apikey and Endpoint are required for gpt client")
        self.azure_client = AzureOpenAI(
            api_version=self.api_version,
            api_key=self.azure_api_key,
            azure_endpoint=self.azure_endpoint
        )

    def request_gpt(self, messages: list[dict[str, str]]) -> Optional[str]:
        """
        request gpts with constructed messages
        :param messages: messages for gpt review
        :return:
          review_content: str, the review response
        """
        gpt_result = self.azure_client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        content = json.loads(gpt_result.to_json())
        if "choices" not in content or not content["choices"]:
            return None
        review_message = content["choices"][0]["message"]["content"]
        logger.info("gpt review message: {0}".format(review_message))
        return str(review_message)
