#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Optional

import github
import requests
from pyfred.model import Environment, ScriptFilterOutput, OutputItem, CacheConfig
from pyfred.workflow import script_filter


def _issues_link_item(host=os.environ.get("github_host")) -> OutputItem:
    return OutputItem(
        title="View issues dashboard on GitHub",
        arg=f"https://{host}/issues",
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
            "q": f"type:issue is:open involves:{github_username}",  # requests library will handle ' ' -> '+'
            "sort": " updated",
        },
        headers={"Authorization": f"BEARER {github.token()}"},
    )

    if not response.ok:
        return ScriptFilterOutput(items=[github.ERROR_RESULT])

    items = [
        OutputItem(
            title=i["title"],
            subtitle=f"#{i['number']}  {github.repo_slug(i['repository_url'])} - {', '.join([l['name'] for l in i['labels']])} ({github.human_date(i['updated_at'])} ago)",
            arg=i["html_url"],
            quicklookurl=i["html_url"],
        )
        for i in response.json()["items"]
    ]

    if items:
        return ScriptFilterOutput(
            items=[*items, _issues_link_item()],
            cache=CacheConfig(seconds=120, loosereload=True),
        )
    return ScriptFilterOutput(items=[github.NO_RESULT, _issues_link_item()])


if __name__ == "__main__":
    main()
