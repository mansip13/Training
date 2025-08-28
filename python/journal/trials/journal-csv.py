# error noticed : incorrect file formats for the data.
import pendulum
import pandas as pd 
import argparse
import os
import csv
import json
import numpy as np
from datetime import datetime

#files 
index_file="journal_index.json"
events_log="events.txt"

#logging and indexing functions 
#loading index
def load_index(index):
    if not os.path.exists(index_file):
        return {}
    with open(index_file,"r")as indf:
        return json.load(indf)

#saving index function
def save_index(index):
    with open(index_file,"a") as indf:
        json.dump(index,indf,indent=4)
        
#event logging function
def log_event(message):
    timestamp=pendulum.now().to_datetime_string()
    with open(events_log,"a") as events_file:
        events_file.write("[{timestamp}] {message}\n")
        

#arg functions 
#add journal entries function
def add_entry(args):
    
    #date handeling
    if args.date:
        try:
            entry_date=datetime.strptime(args.date,"%d/%m/%y").date()
        except ValueError:
            print("Invalid date format. use DD-MM-YYYY")
            return
    else:
        entry_date=pendulum.now().date()
     
    #file topic handeling
    filename=f"{entry_date}_{args.topic}.{args.format}"
    entry_timestamp=pendulum.now().to_iso8601_string()
    entry={"Timestamp": entry_timestamp, "message ":args.message} 
    
    #append or create journal entry
    if args.format =="json":
        if os.path.exists(filename):
            with open(filename,"r") as file:
                data=json.load(file)
                
        else:
            data=[]
            log_event=(f"Created File: {filename}")
        
        #sorting the file in chronological order             
        data.append(entry)
        data=sorted(data,key=lambda x: x["timestamp"])
        
        with open(filename, "w") as file:
            json.dump(data,file,indent=4)
            
    elif args.format=="csv":
        file_exists=os.path.exists(filename)
        with open(filename,"a",newline="")as file:
            writer = csv.DictWriter(file,fieldnames=["timestamp","message"])
            if not file_exists:
                writer.writeheader()
                log_event("Created file: {filename}")
            writer.writerow(entry)
            
        df=pd.read_csv(filename)
        df=df.sort_values(by="timestamp")
        df.to_csv(filename,index=False)
        
    
    index=load_index()
    if filename not in index:
        index[filename] = {
            "created_at":entry_timestamp,
            "last_modified ": entry_timestamp
        }
    else:
        index[filename]["last_modified"]= entry_timestamp
    save_index(index)
    
    
    log_event(f"Appended entry to:{filename}")
    print(f"Entry added to {filename}")


#list journal entries function
def list_journals(args):
    index=load_index()
    if not index:
        print("No journals found")
        return
    
    print("Journal Files:")
    for file,meta in index.items():
        print(f" -{file} (created: {meta['created_at']}, last modeified: {meta:['last_modified']})")

#search journal entries function
def search_journals(args):
    index=load_index()
    if not index:
        print("No journals found")
        return
    
    results=[]
    if args.date:
        for file in index.keys():
            if file.startswith(args.date):
                results.append(file)
    elif args.keyword:
        for file in index.keys():
            if file.endswith(".json"):
                with open(file,"r") as f:
                    data = json.load(f)
                    for entry in data:
                         if args.keyword.lower() in entry["message"].lower():
                             results.append(file)
                             break
            
            elif file.endswith(".csv"):
                df=pd.read_csv(file)
                matches = df[df["message"].str.contains(args.keyword, case=False, na=False)]
                if not matches.empty:
                    results.append(file)
    
    if results:
        print("Matching Files:")
        for r in results:
            print(f" - {r}")
    else:
        print("no match found")

def main():
    parser = argparse.ArgumentParser(description="Journal Logger")
    subparser = parser.add_subparsers(dest="command")
    
    #add parser arg with sub arg 
    add_parser= subparser.add_parser("add",help="Add a new journal Entery")
    add_parser.add_argument("--topic",required=True)
    add_parser.add_argument("--message",required=True)
    add_parser.add_argument("--format",choices=["json","csv"],required=True)
    add_parser.add_argument("--date",help="Specify date (DD-MM-YYY)")
    
    #list arg with sub arg 
    list_parser=subparser.add_parser("list",help="List all Journals")
    
    #search arg with sub arg
    search_parser = subparser.add_parser("search",help="Search Journals")
    search_parser.add_argument("--date",help="Search by date(DD-MM-YYY)")
    search_parser.add_argument("--keyword",help="Search by Keyword")
    
    args=parser.parse_args()
    
    if args.command=="add":
        add_entry(args)
    elif args.command=="list":
        list_journals(args)
    elif args.command=="search":
        search_journals(args)
    else:
        parser.print_help()
        
if __name__ =="main":
    main()



