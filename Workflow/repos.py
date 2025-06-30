#!/usr/bin/env python3

import logging
import os
from pathlib import Path
from typing import Optional

import github
import requests
from pyfred.model import Environment, OutputItem, ScriptFilterOutput, Key, Data
from pyfred.workflow import script_filter

WAITING_ITEM = OutputItem(title="Waiting for query...", valid=False)


@script_filter
def main(
    script_path: Path, args_from_alfred: list[str], env: Optional[Environment]
) -> ScriptFilterOutput:
    if len(args_from_alfred) < 1:
        return ScriptFilterOutput(items=[WAITING_ITEM])
    host = os.environ.get("github_host")

    response = requests.get(
        f"https://{host}/search/repositories",
        params={
            "q": args_from_alfred[0],
        },
        headers={"Authorization": f"BEARER {github.token()}"},
    )

    items = [
        OutputItem(
            title=repo["full_name"],
            arg=repo["html_url"],
            quicklookurl=repo["html_url"],
            autocomplete=repo["full_name"],
            mods={
                Key.Control: Data(
                    arg=[repo["ssh_url"], repo["full_name"]],
                ),
                Key.Option: Data(arg=repo["full_name"]),
            },
        )
        for repo in response.json()["items"]
    ]
    if items:
        return ScriptFilterOutput(items=items)
    return ScriptFilterOutput(items=[github.NO_RESULT])


if __name__ == "__main__":
    main()
