#!/bin/bash
set -e -u
cd "$(dirname "$0")"
rsync -av web_scripts/ /mit/hwops/web_scripts/
chmod 0777 /mit/hwops/web_scripts/robots.txt
