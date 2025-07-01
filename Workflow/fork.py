#!/usr/bin/env python3
import logging
import os
from pathlib import Path
from typing import Optional, Union

import github
import requests
from pyfred.model import Environment
from pyfred.workflow import external_script


@external_script
def main(
    script_path: Path, args_from_alfred: list[str], env: Optional[Environment]
) -> Union[str, list[str]]:
    to_fork = args_from_alfred[0]
    logging.info(f"Preparing to fork {to_fork}")
    prefix = github.rest_prefix(os.environ.get("github_host"))

    response = requests.post(
        f"{prefix}repos/{to_fork}/forks",
        headers={"Authorization": f"BEARER {github.token()}"},
    )
    forked_repo = response.json()
    logging.info(f"Forked repo {forked_repo}")

    if not response.ok:
        return f"ERROR: failed to fork repo. {response.status_code} {response.text}"

    return [forked_repo["ssh_url"], forked_repo["full_name"]]


if __name__ == "__main__":
    main()
