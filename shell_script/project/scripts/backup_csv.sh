#!/bin/sh

src_dir="/home/mansi/project/data"
backup_dir="/home/mansi/project/backups"
log_dir="/home/mansi/project/logs"

DATE=$(date +'%Y-%m-%d_%H-%M-%S')
log_file="$log_dir/backup_$DATE.log"

mkdir -p "$backup_dir" "$log_dir"

echo "===== backup started at ($DATE) =====" > "$log_file"

for file in "$src_dir"/*.csv; do
    if [ -f "$file" ]; then
        base=$(basename "$file" .csv)
        cp "$file" "$backup_dir/${base}_$DATE.csv"
        echo "File Backed up: $file -> ${base}_$DATE.csv" >> "$log_file"
    fi
done 

echo "Running python data wrangling ..." >> "$log_file"
python3 /home/mansi/project/scripts/wrangler.py "$backup_dir" >> "$log_file" 2>&1

echo "===== backup completed ($DATE) =====" >> "$log_file"

