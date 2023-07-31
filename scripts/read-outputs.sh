#!/bin/bash

# Directory to read from
dir=$1

# Ensure the directory path ends with a slash
[[ "$dir" != */ ]] && dir="$dir"/

# Read and output the contents of each file
for file in "${dir}"output-*.json
do
    cat "$file"
done
