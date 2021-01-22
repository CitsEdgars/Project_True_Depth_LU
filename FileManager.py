import os

class FileManager:
    current_location = ""
    res_dir = "\\res"
    settings_dir = "\\settings"

    def __init__(self):
        self.current_location = os.getcwd()

    def get_res_dir(self):
        return self.current_location + self.res_dir

    def get_settings_dir(self):
        return self.current_location + self.settings_dir

    def list_files(self, dir):
        files = os.listdir(dir)
        return files