import os

from source.utils.config_utils import get_config

def get_file_list(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

# Ví dụ sử dụng
folder_path = get_config("image", "gnome")
file_list = get_file_list(folder_path)
print(file_list)
