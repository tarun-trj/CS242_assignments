#!/bin/bash

# Check if exactly 2 arguments are provided
if [ "$#" -ne 2 ]; then								# check number of arguments, if two then proceed to next block
    echo "Error: Correct usage: $0 <search_string> <file_name>"			# output correct usage of this bash script with required arguments
    exit 1									# exit script
fi										# end of conditional block

search_string="$1"								# search string is captured from arguments
file_name="$2"									# file name is captured from arguments

# Check if the file exists and is not empty
if [ ! -f "$file_name" ] || [ ! -s "$file_name" ]; then
    echo "Error: The file '$file_name' does not exist or is empty."		# error output in case file with mentioned filename doesnt exist
    exit 1									# exit script
fi										# end of conditional block

# Loop through each line in the file and search for the string
line_number=1									# variable to store line number
while IFS= read -r line; do							# empty IFS to ignore field separation using whitespace, read lines
    if grep -q "$search_string" <<< "$line"; then				# search for search-string using grep, -q to quieten grep to avoid multiple outputs for same line
        printf "Line Number:%d:\t%s\n" "$line_number" "$line"			# output matched line
    fi
    
    ((line_number++))								# increase line number after each iteration
done < "$file_name"								# loop till file has been exhausted

