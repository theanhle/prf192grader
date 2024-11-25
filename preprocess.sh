#!/usr/bin/env bash

code="./code"
sol="./student_solutions"

mkdir -p $sol
find "$code" -name "*.zip" -exec unzip -o {} -d $sol \;
find $sol -name "*.zip" -exec unzip -o {} -d $sol \;

rm -f $sol/*.zip \;

find $sol -type f -exec mv -f {} $sol \;
find $sol -type d -empty -delete

mkdir -p "$sol/invalid_files"
for file in "$sol"/*; do
    [ -d "$file" ] && continue
    filename=$(basename "$file")
    if [[ ! "$filename" =~ ^[a-z]{2}[0-9]{6}prob[0-9]\.c$ ]]; then
        mv "$file" "$sol/invalid_files"
    fi
done

mkdir -p "$sol/valid_files"
for file in "$sol"/*; do
    [ -d "$file" ] && continue
    filename=$(basename "$file")
    if [[ "$filename" =~ ^[a-z]{2}[0-9]{6}prob([0-9])\.c$ ]]; then
        prob_number="prob${BASH_REMATCH[1]}"
        mkdir -p "$sol/valid_files/$prob_number"
        mv "$file" "$sol/valid_files/$prob_number"
    fi
done
