#!/bin/bash

root_dir=$(pwd);
python_app="$root_dir/Python/python";
phantom_app="$root_dir/phantom/phantom.py";

if [[ -f "$python_app" ]] && [[ -f "$phantom_app" ]]; then
    $python_app $phantom_app "$@" || { echo "Could not open phantom. Please report to Shift Team"; exit 1; }
else
    echo "Missing either python or phantom software. Exiting.";
    exit 1
fi

exit 0
