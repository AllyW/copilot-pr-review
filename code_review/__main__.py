# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

import argparse
from code_review.pr_processor import PRProcessor


def main(job: str) -> None:
    if job == "review":
        PRProcessor().review_pr()
    elif job == "reset":
        pass
    else:
        print("unsupported job type")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", choices=["review", "reset"], required=True, help="job type")
    args = parser.parse_args()
    print(vars(args))
    main(args.job)
