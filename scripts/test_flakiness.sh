#!/bin/bash -e

# Set flag to exit immediately if any command fails
set -e

source venv/bin/activate

# Run the test suite 10 times
for i in {1..10}
do
    time flowthought_run_tests_parallel
done
