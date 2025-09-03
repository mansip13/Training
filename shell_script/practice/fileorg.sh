#!/bin/bash
# File Organizer Script

# Ask user for directory
read -p "Enter the directory to organize: " target_dir

# Check if directory exists
if [ ! -d "$target_dir" ]; then
    echo "Error: Directory does not exist!"
    exit 1
fi

# Go inside directory
cd "$target_dir" || exit

# Loop through files in directory
for file in *; do
    # Skip if it's a directory
    if [ -d "$file" ]; then
        continue
    fi

    # Get file extension (lowercase)
    ext="${file##*.}"
    ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

    # Skip if no extension
    if [ "$ext" = "$file" ]; then
        continue
    fi

    # Make folder for extension if not exists
    mkdir -p "$ext"

    # Move file into that folder
    mv "$file" "$ext/"
done

echo " Files organized by extension inside $target_dir"
