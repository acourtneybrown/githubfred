#!/usr/bin/env python3
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
    api_url = args_from_alfred[0]

    response = requests.patch(
        api_url,
        headers={"Authorization": f"BEARER {github.token()}"},
    )

    if not response.ok:
        return f"ERROR: unable to mark notification read: {response.text}"
    return api_url


if __name__ == "__main__":
    main()
