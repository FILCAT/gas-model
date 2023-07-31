import re
import sys

# Read input from stdin
input_string = sys.stdin.read()

# Regular expression to find all numbers in the string
numbers = re.findall(r'\b\d+\b', input_string)

# Convert all numbers to integers and sum them up
total_sum = sum(map(int, numbers))

print(total_sum)
