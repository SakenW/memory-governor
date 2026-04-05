#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
PUBLISH_DIR="$ROOT_DIR/publish/clawhub"

rm -rf "$PUBLISH_DIR"
mkdir -p "$PUBLISH_DIR"

copy_path() {
  src="$1"
  dst="$PUBLISH_DIR/$1"
  mkdir -p "$(dirname "$dst")"
  if [ -d "$ROOT_DIR/$src" ]; then
    cp -R "$ROOT_DIR/$src" "$dst"
  else
    cp "$ROOT_DIR/$src" "$dst"
  fi
}

copy_path "SKILL.md"
copy_path "README.md"
copy_path "VERSION"
copy_path "LICENSE"
copy_path "CHANGELOG.md"
copy_path "references"
copy_path "assets"
copy_path "scripts/bootstrap-generic-host.sh"
copy_path "scripts/check-memory-host.py"
copy_path "scripts/validate-memory-frontmatter.py"
copy_path "examples/generic-host"

rm -rf "$PUBLISH_DIR/scripts/__pycache__"

printf 'Refreshed ClawHub package at %s\n' "$PUBLISH_DIR"
