#!/usr/bin/env python3
import os
import re
from pathlib import Path
from typing import Optional, List

import github
import requests
from pyfred.model import Environment, OutputItem, ScriptFilterOutput, Key, Data
from pyfred.workflow import script_filter

WAITING_ITEM = OutputItem(title="Waiting for query...", valid=False)
USER_PATTERN = re.compile(r"(?:^|\s*)user:\s*(?P<user>.*?)(?:\s|$)")


def _my_repos_item(
    search_term="",
    username=os.environ.get("github_username"),
) -> OutputItem:
    return OutputItem(
        title=f"Search my repos{' for ' + search_term if search_term else ''}...",
        autocomplete=f"user:{username} {search_term}",
        valid=False,
    )


@script_filter
def main(
    script_path: Path, args_from_alfred: List[str], env: Optional[Environment]
) -> ScriptFilterOutput:
    if not args_from_alfred:
        return ScriptFilterOutput(items=[WAITING_ITEM, _my_repos_item()])
    prefix = github.rest_prefix(os.environ.get("github_host"))

    search_term = args_from_alfred[0]
    response = requests.get(
        f"{prefix}search/repositories",
        params={
            "q": search_term,
        },
        headers={"Authorization": f"BEARER {github.token()}"},
    )

    if not response.ok:
        return ScriptFilterOutput(items=[github.ERROR_RESULT])

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

    extra_items = (
        [_my_repos_item(search_term)] if not USER_PATTERN.match(search_term) else []
    )
    if items:
        return ScriptFilterOutput(items=[*items, *extra_items])
    return ScriptFilterOutput(items=[github.NO_RESULT, *extra_items])


if __name__ == "__main__":
    main()
