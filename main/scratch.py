from utils.file_managers import create_dirs
import os

pwd = os.getcwd()
print(pwd)
new_path = os.path.join(pwd,'/temp/ubnda')
print(new_path)
create_dirs(new_path)