#!/bin/sh
# Build the plugin zip into dist/: upload it in Claude (Customize > Plugins > Add > Upload plugin)
# or ChatGPT (Plugins > Add > Upload a plugin from archive). Its top-level folder holds .claude-plugin/plugin.json.
set -e
cd "$(dirname "$0")/.."
mkdir -p dist
rm -f dist/inkling-plugin.zip dist/inkling-skill.zip
(cd plugins && zip -rq ../dist/inkling-plugin.zip inkling -x "*/__pycache__/*" "*.pyc" "*/.DS_Store")
echo "dist/inkling-plugin.zip"
