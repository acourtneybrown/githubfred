import logging
import os
import subprocess

import humanize
import datetime as dt
from pyfred.model import OutputItem

TOKEN_SHELL_COMMAND = "test -e ~/.zshenv && source ~/.zshenv ; echo $GITHUB_TOKEN"
NO_RESULT = OutputItem(
    title="No response from GitHub",
    subtitle="Try again later.",
    valid=False,
)


def token():
    if (
        "github_token_from_alfred_prefs" in os.environ
        and os.environ["github_token_from_alfred_prefs"].strip()
    ):
        logging.debug("Found GitHub token from 'github_token_from_alfred_prefs'")
        return os.environ["github_token_from_alfred_prefs"]

    if "GITHUB_TOKEN" in os.environ and os.environ["GITHUB_TOKEN"].strip():
        logging.debug("Found GitHub token from environment variable 'GITHUB_TOKEN'")
        return os.environ["GITHUB_TOKEN"]

    logging.debug("Attempting to get GitHub token from 'TOKEN_SHELL_COMMAND'")
    return subprocess.check_output(TOKEN_SHELL_COMMAND, shell=True).decode().strip()


def human_date(date: str) -> str:
    # "pad" the milliseconds section to equivalent microseconds
    return humanize.naturaldelta(
        dt.datetime.now(dt.timezone.utc)
        - dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
    )
