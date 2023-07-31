#!/bin/bash

for file in output/*
do
    if [[ "$file" == *"output-"*  ]]; then
	cat $file | jq -s '.' > tmp.temp
	mv tmp.temp $file
    fi
done

    

