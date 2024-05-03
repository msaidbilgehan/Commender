import os
# import sys

# Imports
# sys.path.append('/path/to/your/main/directory')


app_path = os.path.dirname(__file__) + "/"

# Folder for all Thread/Endpoint files
# root_files_path = app_path + "Files/"
# if not os.path.exists(root_files_path):
#     os.makedirs(root_files_path)

# Folder for all Thread/Endpoint Action Script files
# root_upload_path = app_path + "Upload_Files/"

# Logger Paths
root_path_dir_log = app_path + "logs/"
if not os.path.exists(root_path_dir_log):
    os.makedirs(root_path_dir_log)

root_path_logs = root_path_dir_log + "logs.log"