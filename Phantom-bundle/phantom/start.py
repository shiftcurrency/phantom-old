#!/usr/bin/env python2.7


# Included modules
import sys

# Phantom Modules
import phantom


def main():
    sys.argv += ["--open_browser", "default_browser"]
    phantom.main()

if __name__ == '__main__':
    main()
