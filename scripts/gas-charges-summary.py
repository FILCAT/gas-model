import sys
import json
from collections import defaultdict

# Reads JSON data from standard input
input_data = sys.stdin.read()

# Parse the JSON data
data = json.loads(input_data)

# Create a default dictionary to store the sum of 'tg' for each 'Name'
summary = defaultdict(int)

# Iterate over the 'GasCharges' array
for obj in data.get('GasCharges', []):
        # Update the 'tg' sum for each 'Name'
        summary[obj['Name']] += obj['tg']

# Print the summary
for name, tg_sum in summary.items():
        print(f"{name}: {tg_sum}")
                
