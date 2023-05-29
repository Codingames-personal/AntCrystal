import os

def del_last_line(file_path : str) -> None:
    with open(file_path, 'r') as file:
        file_list = list(file.readlines())
    
    with open(file_path, 'w') as file:
        for file_line in file_list[:-1]:
            file.write(file_line)

def write_after(file_path : str, line : str) -> None:
    with open(file_path, 'a') as file:
        file.write(line)

def is_empty(file_path):
    """
    If file_path is the path of a folder, verify if there is something inside
    if it is a script verify if it is empty
    """
    if os.path.isdir(file_path):
        return list(os.listdir(file_path)) == []
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            return list(file.readlines()) == []
    