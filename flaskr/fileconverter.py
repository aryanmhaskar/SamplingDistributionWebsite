import os, csv
import pandas as pd

def process_text(filename:str):
    my_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads/')  + filename, "r")
    content = my_file.read()
    content_list = content.split(",")
    #refine the list a little bit
    for val in content_list:
        if val == '':
            content_list.remove(val)
    my_file.close()
    return content_list

def convert_csv(filename):
    data = []
    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            for item in row:
                try:
                    data.append(float(item))     
                except:
                    print()      
    return data

def convert_xl(filename):
    if (filename[-3:] == "csv"):
        convert_csv(filename)
    read_file = pd.read_excel(filename)
    read_file.to_csv("converted.csv", index = None, header=True)
    return convert_csv("converted.csv")