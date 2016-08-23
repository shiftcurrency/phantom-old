#!/bin/bash

cd "$(dirname "$0")"
if [ x$DISPLAY != x ] || [[ "$OSTYPE" == "darwin"* ]]; then
    # Has gui, open browser
    SCRIPT="start.py"
else
    # No gui
    SCRIPT="phantom.py"
fi

if [ -d "phantom" ]; then
    cd "$(dirname "$0")/phantom"
    ../Python/python $SCRIPT "$@"
fi
