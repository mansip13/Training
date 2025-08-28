import pendulum
import argparse

#cli options setup 
parser =argparse.ArgumentParser(description="Daily Journal Logger")
parser.add_argument("--tz", type=str,help="Timezone( e.g. Asia/Kolkata, US/Eastern)")
parser.add_argument("--show", action="store_true",help="Show All Journal entries")

args=parser.parse_args()


#showing all entries 

if args.show:
    try:
        with open("journal_pendulum.txt","r") as file: 
            entries=file.readlines()
            if not entries:
                print("No Journal Entries Yet")
            else:
                print("Your Journal entries: ")
                for line in entries:
                    print(line.strip())
    except FileNotFoundError:
        print("No Journal Found!")               
else:
    

    #timezone setting
    if args.tz:
        now=pendulum.now(args.tz)
    else:
        now=pendulum.now()
        
    #jounral input
    journal_entry=input("Journal Entry: ")
        
    #formatting date time: 
    timestamp = now.format("HH:mm:ss DD/MM/YYYY")
    #file manip
    with open("journal_pendulum.txt","a") as file:
        file.write(f"{timestamp} : {journal_entry}\n")