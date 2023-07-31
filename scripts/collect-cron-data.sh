#!/bin/bash

# Get the current chain height from the Lotus node
current_height=$(./lotus chain getblock $(./lotus chain head | head -n 1) | jq ".Height")

# Set the number of past epochs to process
num_epochs=$1

# Set the output directory
output_dir=$2

# Ensure the output directory ends with a slash
[[ "$output_dir" != */ ]] && output_dir="$output_dir"/

# Ensure that the output directory exists
mkdir -p "$output_dir"

# Iterate over the past epochs
for (( i=1; i<=$num_epochs; i++ ))
do
    # Calculate the target epoch
    target_epoch=$((current_height - i))

    # Run the cron-data.sh script
    ./cron-data.sh "$target_epoch" "$output_dir"
done
