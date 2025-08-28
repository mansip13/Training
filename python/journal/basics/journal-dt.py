from datetime import datetime
#JOURNAL ENTRY
journal_entry=input("Journal entry: ")

#setting up time logs
entry_time= datetime.now()
timestamp = entry_time.strftime("%H:%M:%S %d-%m-%Y")


#appending to txt file
with open("journal.txt","a") as file:
    file.write(f"{timestamp}:{journal_entry}\n")
    
print("Entry Saved")

