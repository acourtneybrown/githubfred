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


@script_filter
def main(
    script_path: Path, args_from_alfred: list[str], env: Optional[Environment]
) -> ScriptFilterOutput:
    host = os.environ.get("github_host")

    response = requests.get(
        f"https://{host}/notifications",
        headers={"Authorization": f"BEARER {github.token()}"},
    )

    if not response.ok:
        return ScriptFilterOutput(items=[github.NO_RESULT])

    items = [
        OutputItem(
            title=n["subject"]["title"],
            subtitle=f"{n['repository']['full_name']}  ({github.human_date(n['updated_at'])} ago)",
            arg=n["subject"]["url"],
            mods={Key.Control: Data(arg=n["id"])},
        )
        for n in response.json()
    ]

    if items:
        return ScriptFilterOutput(
            items=items, cache=CacheConfig(seconds=120, loosereload=True)
        )
    return ScriptFilterOutput(items=[github.NO_RESULT])


if __name__ == "__main__":
    main()
