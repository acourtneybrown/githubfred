#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Optional

import github
import requests
from pyfred.model import (
    Environment,
    ScriptFilterOutput,
    OutputItem,
    CacheConfig,
    Key,
    Data,
)
from pyfred.workflow import script_filter


def _notifications_link_item(host=os.environ.get("github_host")) -> OutputItem:
    return OutputItem(
        title="View notifications dashboard on GitHub",
        arg=["html", f"https://{host}/notifications"],
    )


@script_filter
def main(
    script_path: Path, args_from_alfred: list[str], env: Optional[Environment]
) -> ScriptFilterOutput:
    prefix = github.rest_prefix(os.environ.get("github_host"))

    response = requests.get(
        f"{prefix}notifications",
        headers={"Authorization": f"BEARER {github.token()}"},
    )

    if not response.ok:
        return ScriptFilterOutput(items=[github.ERROR_RESULT])

    items = [
        OutputItem(
            title=n["subject"]["title"],
            subtitle=f"{n['repository']['full_name']}  ({github.human_date(n['updated_at'])} ago)",
            arg=["api", n["subject"]["url"]],
        )
        for n in response.json()
    ]

    if items:
        return ScriptFilterOutput(
            items=[*items, _notifications_link_item()],
            cache=CacheConfig(seconds=120, loosereload=True),
        )
    return ScriptFilterOutput(items=[github.NO_RESULT, _notifications_link_item()])


if __name__ == "__main__":
    main()
