#!/bin/bash

# A simple wrapper around LKH that takes arguments on the command-line
# instead of in a parameter file.

LKH=LKH-2.0.7/LKH

tempfile=$(mktemp)
cleanup() { rm -f "$tempfile"; }
trap cleanup EXIT

cat >"$tempfile" <<END
PROBLEM_FILE = tsp/instance/cities.tsp
OUTPUT_TOUR_FILE = tsp/tour/$1
SEED = 1
TRACE_LEVEL = 2
END

"$LKH" "$tempfile"
