# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

import unittest
from code_review.util import filter_review_patch_pattern


class UtilTestCase(unittest.TestCase):
    def test_filter_review_patch(self):
        text = """
        @@ -2,6 +2,10 @@
        Some changes here
        @@ -12,4 +12,6 @@
        More changes here
        @@ -30,10 +30,12 @@
        Another change
        """
        res = filter_review_patch_pattern(text)
        self.assertEqual(res, False, "error in filter patch body")


if __name__ == '__main__':
    unittest.main()
