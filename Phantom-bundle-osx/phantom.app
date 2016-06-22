#!/bin/bash
cd "$(dirname "$0")"
if [ -d "phantom" ]; then
    cd "$(dirname "$0")/phantom"
    ../Python/python phantom.py "$@"
fi
