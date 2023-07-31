#!/bin/bash


# Gather gas traces from lotus API, persist gas traces
# Process ~50MB of gas traces into ~10kB cron job gas summaries
#   Arguments
#      - $1 epochs from head to collect gas traces from
#      - $2 directory to write files to
#
# To collect other data modify script to call an alternative to cron-data.sh
# collecting message data from the relevant messages.
# The gas summary datastructure should generally stay the same.
# You'll need to call a new or modified lotus-shed command for relevant state variables.
./scripts/collect-cron-data.sh 1000 output

# Gather summary data and transform into vector data for modeling
#
# To process other data modify vectorize-cron-jobs.py to take in gas/state summaries
# from other messages and parse these into the desired vector format
python3 ./scripts/vectorize-cron-jobs.py output/output.csv (ls output/* | grep "output-")

# Read in vector data and perform regression on model
#
# To model other message gas costs you'll want to match the vector structure
# of the csv defined in the modified `vectorize-cron-jobs` script
python3 mlinear-regression.py output/output.csv





