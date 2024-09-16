# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------


class InvalidOpenAIConfigException(Exception):
    """Still an exception raised when uncommon things happen"""
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return str(self.message)


class InvalidGitTokenMissingException(Exception):
    pass


class OtherConfigMissingException(Exception):
    pass
