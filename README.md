# Alfred GitHubFred

Helpful GitHub assistant for Alfred

## Usage

- Search GitHub repositories (public only without [GitHub Token](#github-token) set) via the keyword `gh`.
	+ <kbd>⏎</kbd>: Open the repo's GitHub page.
	+ <kbd>⌘C</kbd>: Copy the repo URL.
	+ <kbd>⌃⏎</kbd>: Clone the repo to a local folder and open in the Terminal.
	+ <kbd>⌥⏎</kbd>: Fork the repo & clone the fork to a local folder. Then open in Terminal.
- Access pull requests you have opened with keyword `ghpr`.
	+ <kbd>⏎</kbd>: Open the PR in the browser.
	+ <kbd>⌘C</kbd>: Copy the PR URL.
- Open recent GitHub issues you are involved in with `ghi`.
	+ <kbd>⏎</kbd>: Open the issue in the browser.
	+ <kbd>⌘C</kbd>: Copy the issue URL.
- Access your GitHub notifications list with keyword `ghn`.
	+ <kbd>⏎</kbd>: Open the notification in the browser.
	+ <kbd>⌃⏎</kbd>: Mark the notification as read.
    + <kbd>⌃⏎</kbd>: Mark the notification as done.
	+ <kbd>⌘C</kbd>: Copy the notification's API URL.

The `gh` prefix can be changed in the configuration page, thus affecting all the keywords.

## GitHub Token

1. Add the **GitHub Token** in the Alfred workflow configuration.
2. Or: export the token in your `.zshenv`.

```zsh
# add this to your `$HOME/.zshenv`
# ($alfred_workflow_name is only populated by shell processes that called by Alfred)
if [[ "$alfred_workflow_name" == "GitHubFred" ]]; then
	# if using a password manager, you can do something like this 
	# (`op` being the CLI for 1Password)
	GitHub_SERVER_TOKEN=$(op read "op://vault/GitHub.com/token")
	export GitHub_SERVER_TOKEN
fi
```

## Installation

[➡️ Download the latest release](https://github.com/acourtneybrown/GitHubFred/releases)
