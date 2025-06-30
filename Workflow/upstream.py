#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from typing import Optional, Union
from urllib.parse import quote_plus

import github
import requests
from pyfred.model import Environment
from pyfred.workflow import external_script


@external_script
def main(
    script_path: Path, args_from_alfred: list[str], env: Optional[Environment]
) -> Union[str, list[str]]:
    (repo, abs_path) = args_from_alfred
    host = os.environ.get("github_host")

    response = requests.get(
        f"https://{host}/repos/{repo}",
        headers={"PRIVATE-TOKEN": github.token()},
    )
    json = response.json()

    if not response.ok:
        return f"ERROR: unable to fetch repo info: {json}"

    if "parent" in json:
        if (
            subprocess.call(
                [
                    "git",
                    "remote",
                    "add",
                    "upstream",
                    json["parent"]["ssh_url"],
                ],
                cwd=abs_path,
            )
            != 0
        ):
            return "ERROR: failed to set upstream"

        if subprocess.call(["git", "fetch", "upstream"], cwd=abs_path) != 0:
            return "ERROR: failed to fetch upstream"

    return abs_path


if __name__ == "__main__":
    main()
