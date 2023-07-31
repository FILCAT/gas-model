import json
import csv
import sys

def get_data_from_file(file_name):
    with open(file_name, 'r') as file:
        json_object = json.load(file)
        # Assume that the JSON object is a list
        for item in json_object:
            yield item


def process_json(json_objects):
    data = []
    for json_object in json_objects:
        x1 = x2 = x3 = x6 = x7 = x8 = 0
        partitions = json_object.get("Partitions", [])
        if partitions is not None:
            for partition in partitions:
                if partition.get("Live", 0) > 0:
                    x1 += 1
                if partition.get("Faulty", 0) > 0:
                    x2 += 1
                if partition.get("Diff", {}).get("Faulted", 0) > 0:
                    x3 += 1
                x6 += partition.get("Diff", {}).get("Killed", 0)
            if x1 > 0:
                x7 = 1
            if x2 > 0:
                x8 = 1

        x4 = len(json_object.get("PreCommitExpiry", {}).get("Expired", []) or [])
        x5 = json_object.get("VestingDiff", {}).get("PrevTableSize", 0)

        row = [json_object.get("To"), json_object.get("Height"), json_object.get("Gas", {}).get("tg"),
               x1, x2, x3, x4, x5, x6, x7, x8]
        data.append(row)
    return data

def main(input_files, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Address', 'Height', 'TotalGas', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8'])        
        
        for input_file in input_files:
            print(input_file)
            json_objects = get_data_from_file(input_file)
            data = process_json(json_objects)
            writer.writerows(data)

# Usage
if len(sys.argv) < 3:
    print("Expect > 2 arguments, output.csv and input files")
else:
    main(sys.argv[2:], sys.argv[1])

