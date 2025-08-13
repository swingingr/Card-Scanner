# Used exclusively for changing names in the hash database to match the format from my personal databse

import csv
import cv2 
import pandas as pd



def change_csv_item(file_path, old_name, new_name):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    for i in range(len(data)):
        if data[i][1] == old_name:
            data[i][1] = new_name
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    """
    Changes a specific item in a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        row_index (int): Index of the row to modify (0-based).
        column_index (int): Index of the column to modify (0-based).
        new_value (any): The new value to set.
    """


# Example
file_path = 'SetData copy.csv'
old_name = 'Team Magma vs Team Aqua'
new_name = 'EX Team Magma vs Team Aqua'
change_csv_item(file_path, old_name, new_name)