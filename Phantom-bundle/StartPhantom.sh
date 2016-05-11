#!/bin/bash
cd "$(dirname "$0")"
    SCRIPT="phantom.py"

if [ -d "phantom" ]; then
    cd "$(dirname "$0")/phantom"
    ../Python/python $SCRIPT "$@"
fi
