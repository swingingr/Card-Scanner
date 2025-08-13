from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity
from pokemontcgsdk import RestClient
import csv
from imagehash import hex_to_hash
import cv2 



import pandas as pd
import ast




def append_column_csv(filename, new_column_data, new_column_name):
    """Appends a column to an existing CSV file."""
    rows = []
    with open(filename, 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        for i, row in enumerate(reader):
            bar = (hex_to_hash(row[10]).hash.flatten().tolist() + hex_to_hash(row[14]).hash.flatten().tolist()) #This is what is used to check hamming distance formula
            str=""
            for i in range(len(bar)):
                if bar[i] == True:
                    str = str + "1"
                if bar[i] == False:
                    str = str + "0"
            print(str)
            row.append(str)
            rows.append(row)
    with open(filename, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

# Example usage
filename = 'SetData copy.csv'
new_column_name = 'New Column'
new_column_data = ['value1', 'value2', 'value3']
append_column_csv(filename, new_column_data, new_column_name)

RestClient.configure('7db61996-e6d4-455b-89aa-f1bf2f71b4fa')

