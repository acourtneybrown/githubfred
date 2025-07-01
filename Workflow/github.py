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
ERROR_RESULT = OutputItem(
    title="Error result from GitHub",
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


def repo_slug(repo: str) -> str:
    """Extracts the repo slug from a `repository_url` field in a response"""
    return "/".join(repo.split("/")[-2:])


def _auth_normalize(hostname: str) -> str:
    if hostname.endswith(".github.com"):
        return "github.com"
    if hostname.endswith(".github.localhost"):
        return "github.localhost"
    if hostname.endswith(".ghe.com"):
        return ".".join(hostname.split(".")[-3:])
    return hostname


def _auth_is_enterprise(hostname: str) -> bool:
    hostname = _auth_normalize(hostname)
    return (
        hostname != "github.com"
        and hostname != "github.localhost"
        and not hostname.endswith(".ghe.com")
    )


def rest_prefix(hostname: str) -> str:
    """
    Given a hostname as would be passed as --hostname argument to `gh`,
    translate it into the prefix for URLs used to interact with the
    GitHub instance's REST API.

    See: https://github.com/cli/go-gh/blob/a08820a13f257d6c5b4cb86d37db559ec6d14577/pkg/api/rest_client.go#L160
    """
    if hostname.casefold() == "garage.github.com".casefold():
        return f"https://{hostname}/api/v3/"
    hostname = _auth_normalize(hostname)
    if _auth_is_enterprise(hostname):
        return f"https://{hostname}/api/v3/"
    if hostname.casefold() == "github.localhost".casefold():
        return f"https://api.{hostname}/"
    return f"https://api.{hostname}/"
