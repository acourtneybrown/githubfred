#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Optional

import github
import requests
from pyfred.model import Environment, ScriptFilterOutput, OutputItem, CacheConfig
from pyfred.workflow import script_filter


def _pr_link_item(host=os.environ.get("github_host")) -> OutputItem:
    return OutputItem(
        title="View pull reqeust page on GitHub",
        arg=f"https://{host}/pulls",
    )


@script_filter
def main(
    script_path: Path, args_from_alfred: list[str], env: Optional[Environment]
) -> ScriptFilterOutput:
    prefix = github.rest_prefix(os.environ.get("github_host"))
    github_username = os.environ.get("github_username")

    response = requests.get(
        f"{prefix}search/issues",
        params={
            "q": f"type:pr is:open author:{github_username}",  # requests library will handle ' ' -> '+'
            "sort": " updated",
        },
        headers={"Authorization": f"BEARER {github.token()}"},
    )

    if not response.ok:
        return ScriptFilterOutput(items=[github.ERROR_RESULT])

    def is_draft(draft: bool) -> str:
        return "🟡" if draft else "🟢"

    items = [
        OutputItem(
            title=f"{is_draft(pr['draft'])} {pr['title']}",
            subtitle=f"#{pr['number']} {github.repo_slug(pr['repository_url'])} ({github.human_date(pr['updated_at'])} ago)",
            arg=pr["html_url"],
            quicklookurl=pr["html_url"],
        )
        for pr in response.json()["items"]
    ]

    if items:
        return ScriptFilterOutput(
            items=[*items, _pr_link_item()],
            cache=CacheConfig(seconds=120, loosereload=True),
        )
    return ScriptFilterOutput(items=[github.NO_RESULT, _pr_link_item()])


if __name__ == "__main__":
    main()
