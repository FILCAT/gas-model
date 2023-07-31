import pandas as pd
import sys

def filter_csv(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Filter rows where x4 is not equal to zero
    df_filtered = df[df['x4'] == 0]

    # Write the filtered dataframe to the output CSV file
    df_filtered.to_csv(output_file, index=False)

if len(sys.argv) < 3:
    print("Expect > 2 arguments, output.csv and input.csv")
else:
    filter_csv(sys.argv[1], sys.argv[2])
