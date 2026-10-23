#!/bin/sh
# Build the two claude.ai upload zips into dist/.
#   inkling-plugin.zip: Customize > Plugins > Add > Upload plugin (top-level folder holds .claude-plugin/plugin.json)
#   inkling-skill.zip:  Customize > Skills > Upload a skill (top-level folder holds SKILL.md)
set -e
cd "$(dirname "$0")/.."
mkdir -p dist
rm -f dist/inkling-plugin.zip dist/inkling-skill.zip
EXCLUDE="-x */__pycache__/* *.pyc */.DS_Store"
(cd plugins && zip -rq ../dist/inkling-plugin.zip inkling $EXCLUDE)
(cd plugins/inkling/skills && zip -rq ../../../dist/inkling-skill.zip inkling $EXCLUDE)
echo "dist/inkling-plugin.zip"
echo "dist/inkling-skill.zip"
