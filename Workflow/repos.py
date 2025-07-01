#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Optional

import github
import requests
from pyfred.model import Environment, OutputItem, ScriptFilterOutput, Key, Data
from pyfred.workflow import script_filter

WAITING_ITEM = OutputItem(title="Waiting for query...", valid=False)


def _my_repos_item(
    search_term="",
    username=os.environ.get("github_username"),
) -> OutputItem:
    search_term_without_user = search_term.removeprefix(f"{username}/")
    return OutputItem(
        title=f"Search my repos{' for ' + search_term_without_user if search_term_without_user else ''}...",
        autocomplete=f"{username}/{search_term_without_user}",
        valid=False,
    )


@script_filter
def main(
    script_path: Path, args_from_alfred: list[str], env: Optional[Environment]
) -> ScriptFilterOutput:
    if len(args_from_alfred) < 1:
        return ScriptFilterOutput(items=[WAITING_ITEM, _my_repos_item()])
    host = os.environ.get("github_host")

    search_term = args_from_alfred[0]
    response = requests.get(
        f"https://{host}/search/repositories",
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
    if items:
        return ScriptFilterOutput(items=[*items, _my_repos_item(search_term)])
    return ScriptFilterOutput(items=[github.NO_RESULT, _my_repos_item(search_term)])


if __name__ == "__main__":
    main()
