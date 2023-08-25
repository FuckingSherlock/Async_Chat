import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
files = [
    'client_read.py', 'client_start.py', 'client_write.py', 'client_meta.py', 'client_db.py', 'gui_login.py', 'gui_main.py', 'descr.py', 'server_meta.py', 'server.py', 'server_db.py']


def create_file_names(list_of_files):
    for file in list_of_files:
        with open(file, 'w') as f:
            f.write(f'.. automodule:: {file[0:-3]}\n    :members:')

        os.rename(file, file.replace('.py', '.rst'))


create_file_names(files)
