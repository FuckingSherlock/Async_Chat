import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
files = [
    'client_read.py', 'client_start.py', 'client_write.py', 'client_meta.py', 'client_db.py', 'gui_login.py', 'gui_main.py', 'descr.py', 'server_meta.py', 'server.py', 'server_db.py']

for file in files:

    print(file[0:-3])

# def create_file_names(list_of_files):
#     for file in list_of_files:
#         with open(file, 'w') as f:
#             f.write(f'.. automodule:: {file[0:-3]}\n    :members:')

#         os.rename(file, file.replace('.py', '.rst'))


# create_file_names(files)
".\client\client_meta.py"
".\client\client_read.py"
".\client\client_start.py"
".\client\client_write.py"
".\client\client_database\client_db.py"
".\client\client_gui\gui_login.py"
".\client\client_gui\gui_main.py"
".\documentation\source\conf.py"
".\server\descr.py"
".\server\server.py"
".\server\server_meta.py"
".\server\server_database\server_db.py"
