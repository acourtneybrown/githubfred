#!/usr/bin/env zsh

ssh_url="$1"
clone_dir="$2"

# shellcheck disable=SC2154
[[ -z "$local_repo_root" ]] && local_repo_root="$HOME/$github_host"
[[ ! -d "$local_repo_root" ]] && mkdir -p "$local_repo_root"
cd "$local_repo_root" || return 1

if ! msg=$(git clone "$ssh_url" "$clone_dir" 2>&1); then
  echo "ERROR: Clone failed. $msg"
  return 1
fi

# Open in terminal via Alfred
abs_path="$local_repo_root/$clone_dir"
echo -n "$clone_dir $abs_path"
