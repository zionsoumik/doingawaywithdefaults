#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
	python main1.py 3 6 $line 
done< "$1"
