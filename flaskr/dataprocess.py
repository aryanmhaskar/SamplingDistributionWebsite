import os

def process_text(filename:str):
    my_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads/')  + filename, "r")
    content = my_file.read()
    content_list = content.split(",")
    #refine the list a little bit
    for val in content_list:
        if val == '':
            content_list.remove(val)
    my_file.close()
    print(content_list)

def process_csv():
    return

process_text("EDISTSCORES.txt")