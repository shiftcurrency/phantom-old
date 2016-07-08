#!/bin/bash

root_dir=$(pwd);
python_app="../Python/python";
phantom_dir="$root_dir/phantom/"

if [[ -f "$python_app" ]] && [[ -d "$phantom_dir" ]]; then
    cd $phantom_dir && $python_app phantom.py "$@" || { echo "Could not open phantom. Please report to Shift Team"; exit 1; }
else
    echo "Missing either python or phantom software. Exiting.";
    exit 1
fi

exit 0
