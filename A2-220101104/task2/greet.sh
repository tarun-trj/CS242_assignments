#!/bin/bash

# Check if exactly one argument is provided
if [ "$#" -ne 1 ]; then									# $# stores number of arguments
    echo "Usage: $0 <message_file>"							# correct usage if arguments are invalid
    exit 1										# exit script
fi											# end of conditional statement

message_file="$1"

# Check if the argument is a readable file
if [ ! -r "$message_file" ]; then							# if file cannot be read
    echo "Error: The argument '$message_file' is not a readable file."			# return error
    exit 1										# exit script
fi											# end of conditional statement

# Check if the message file is empty
if [ ! -s "$message_file" ]; then							# check whether file is empty
    echo "Error: The message file '$message_file' is empty."				# return error on empty file
    exit 1										# exit script
fi											# end of conditional statement

# Get a list of logged-in users and store their usernames in a temporary file
who | awk '{print $1}' | sort -u > tmp_users.txt					# get a temp file of users using who command and awk script, sort unique users

# Read the message from the message file
message=$(<"$message_file")								# store messages in message variable

# Send the message to each logged-in user
while IFS= read -r user; do								# read input file lines into user variable 
    # Skip the current user (you)
    if [ "$user" != "$USER" ]; then							# send message to user if applicable
        write "$user" <<<"$message"
    fi
    
    # greet yourself
    if [ "$user" == "$USER" ]; then							# cannot send messages to oneself using write command hence echo message
    	myhostname=$(hostname)
    	printf "Message from $user@$myhostname:\n"
        echo "$message"									# write message to yourself
    fi
done < tmp_users.txt									# take input till its available from the temp file

# Clean up the temporary file
rm tmp_users.txt									# delete temporary file

