##
#%%
import os
import sys

command_list = ['merge']

main_folder_path = __file__[:-16]
src_path = os.path.join(main_folder_path, "src")

folder_path_list = [src_path]

class merge:

    def is_ignore(file_name : str) -> bool:

        with open(os.path.join(main_folder_path, "cgignore"), 'r') as cgignore:
            for ignore_file in cgignore.readlines():
                if ignore_file == file_name: #If the script is directly in cgignore
                    return True
                
                if  os.path.dirname(file_name) == ignore_file: # If the script is in a folder named in cgignore
                    return True

            return False


    def update_folder_path_list() -> None:
        with open(os.path.join(main_folder_path, "cgfolder"), 'r') as cgfolder:
            for folder_name in cgfolder.readlines():
                folder_path = os.path.join(main_folder_path, folder_name)
                if not folder_path in folder_path_list:
                    folder_path_list.append(folder_path)    

    def script_in_order() -> list:
        scripts = []
        for folder_path in folder_path_list:
            for file_path in os.listdir(folder_path):
                if file_path[-3:] == ".py" and not merge.is_ignore(file_path):
                    with open(os.path.join(src_path, file_path), "r") as script:
                        first_line = script.readline()
                        number_index = first_line.index("order :") + len("order :")
                        number = ""
                        while not first_line[number_index].isdigit(): number_index+=1
                        while number_index < len(first_line) and first_line[number_index].isdigit():
                            number+=first_line[number_index]
                            number_index +=1
                        if not number : 
                            raise Exception("Not okay")
                        
                    scripts.append({'file_path' :os.path.join(src_path, file_path), 'order' : number})
        
        
        return list(map(
            lambda script : script['file_path'],
            sorted(
                scripts,
                key=lambda script : script['order'])
                )
            )
    

            
    def copy_files(path_to_copy : str, path_to_paste : str) -> None:
        with open(path_to_copy, "r") as copy_,  open(path_to_paste, "a") as past_:
            for line in copy_.readlines():
                past_.write(line)
            past_.write('\n')
            
        print("copy {} : ok".format(path_to_copy.split("/")[-1]), file=sys.stderr)


    def merge_scripts(scripts : list) -> None:
        main_path = os.path.join(main_folder_path, "main.py")
        open(main_path, "w").close()
        for script_path in scripts:
            merge.copy_files(script_path, main_path)

        print("main.py recreated : ok", file=sys.stderr)


    def execute() -> None:
        print("Starting merge", file=sys.stderr)

        merge.update_folder_path_list()
        print("take into account cgfolder", file=sys.stderr)

        scripts_in_order = merge.script_in_order()
        print("Order the scripts : ok", file=sys.stderr)


        merge.merge_scripts(scripts_in_order)
        print("Scripts have been merged", file=sys.stderr)


    

        
# %%
