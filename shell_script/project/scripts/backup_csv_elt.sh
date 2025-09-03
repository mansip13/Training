#!/bin/bash

src_dir="/home/mansi/project/data"
backup_dir="/home/mansi/project/backups"
log_dir="/home/mansi/project/logs"

DATE=$(date +'%Y-%m-%d_%H-%M-%S')
log_file="$log_dir/backup_$DATE.log"

echo "============= Backup started at $DATE =============" > "$log_file"

# Ensure dirs exist
mkdir -p "$backup_dir" "$log_dir"

# Extract + Load: copy raw CSVs
for file in "$src_dir"/*.csv; do
    if [ -f "$file" ]; then
        base=$(basename "$file" .csv)
        cp "$file" "$backup_dir/${base}_$DATE.csv"
        echo "Copied: $file → ${base}_$DATE.csv" >> "$log_file"
    fi
done

# Transform: run Python wrangler on backup_dir
echo "Running Python transformations..." >> "$log_file"
python3 /home/mansi/project/scripts/wrangler.py "$backup_dir" >> "$log_file" 2>&1

echo "============= Backup completed at $DATE =============" >> "$log_file"

