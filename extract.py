#!/usr/bin/env python3

import sys

from extractor.extractor import extract_bundle

if __name__ == "__main__":
    extract_bundle(sys.argv[1:])
