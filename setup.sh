#!/bin/bash

# provide usage information
usage () {
    echo "Usage: setup.sh <year> [day]"
    echo "  year: year of advent of code"
    echo "  day: day of advent of code"
    echo "  if no day is given, all days can be created"
}

# show usage on h flag or no arguments
if [ "$1" == "-h" ] || [ "$1" == "--help" ] || [ -z "$1" ]; then
    usage
    exit 0
fi

# read year from argument
year=$1

# check if year is given
if [ -z "$year" ]; then
    echo "No year given." 
    exit 1
fi

echo "Setting up year $year"

# create directory
mkdir -p $year
echo "Directory $year created."

# function to create day
create_day () {
    day=$1
    if [ $day -lt 10 ]; then
        day="0${day}"
    fi
    filename="${year}/day${day}.py"
    if [ -f "$filename" ]; then
        echo "File $filename already exists."
    else
        cp template.py $filename
        echo "File $filename created."
    fi
}

day=$2
if [ -z "$day" ]; then
    echo "No day given."

    echo "create all days? (Y/n)"
    read answer
    if [ "$answer" != "${answer#[Nn]}" ] ;then
        exit 0
    else
        for day in {1..25}
        do  
            create_day $day
        done
    fi
else
    if [ $day -lt 1 ] || [ $day -gt 25 ]; then
        echo "Day $day is not in range [1, 25]."
        exit 1
    fi

    create_day $day
    exit 0
fi