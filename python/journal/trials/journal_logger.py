import pendulum
import pandas as pd 
import argparse
import os
import csv
import json
import numpy as np
from datetime import datetime



#functions
#file creation function: 

def create_file(args):
    with open("test.{format}","a") as file:
        json.dump("hi",file,indent=4)    





def main():
    parser = argparse.ArgumentParser(description="Journal Logger")
    subparser = parser.add_subparsers(dest="command")
    
    parser.add_argument("format",required=True,help="Specify the file format(json/csv)")
    
    
    args=parser.parse_args()
    if args.command=="format":
        create_file()
        
    else:
        parser.print_help()   
        
        
    journal_entry=input("Journal Entry: ")     
if __name__ =="main":
    main()
