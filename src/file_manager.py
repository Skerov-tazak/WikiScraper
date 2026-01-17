import pandas
import json
import os
from pathlib import Path

class FileManager:

    @staticmethod
    def get_target_dir(directory):
        current = Path.cwd()
        if current.name == "src":
            dir = current.parent / directory
            dir.mkdir(parents=True, exist_ok=True)
            return dir 
        else:
            dir = Path(directory)
            dir.mkdir(parents=True, exist_ok=True)
            return dir

    @staticmethod
    def remove_file(filepath):
        if os.path.exists(filepath):
            os.remove(filepath)
        else: 
            raise Exception(f"\nFile {filepath} cannot be deleted - it doesn't exist!\n")

    @staticmethod
    def get_file_name(filepath):
        fileparts = filepath.split("/")
        file = fileparts[len(fileparts) - 1]
        return file

    @staticmethod
    def get_article_name(filepath):
        return FileManager.get_file_name(filepath).split(".")[0]


    @staticmethod
    def load_csv_to_pandas(filename, directory="csv"):
        dir = FileManager.get_target_dir(directory)
        filepath = dir / filename
        return pandas.read_csv(filepath)
    
    @staticmethod
    def load_txt(filename, directory="txt"):
        dir = FileManager.get_target_dir(directory)
        filepath = dir / filename
        full_list = []
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for l in lines:
                full_list.append(l.split(" ")[-1].replace("\n",""))
        return full_list

    @staticmethod
    def load_json(filename, directory="json"):
        dir = FileManager.get_target_dir(directory)
        filepath = dir / filename
        return json.load(open(filepath))

    @staticmethod
    def save_csv(filename, data_frame, header=False, directory="csv", extension=".csv", mode='w'):
        filename = filename + extension
        dir = FileManager.get_target_dir(directory)
        filepath = dir / filename
        data_frame.to_csv(filepath, mode=mode, header=header)
        return filepath

    @staticmethod
    def save_json(filename, content, directory="json", extension=".json", mode='w'):
        filename = filename + extension
        dir = FileManager.get_target_dir(directory)
        filepath = dir / filename
        
        if mode == 'a' and os.path.exists(filepath):
            with open(filepath, mode='r', encoding="utf-8") as file:
                old_content = json.load(file)
                content["total"] += old_content["total"]
                for word in old_content["list"]:
                    if word in content["list"]:
                        content["list"][word] += old_content["list"][word]
                    else:
                        content["list"].update({word: old_content["list"][word]})
                    
        with open(filepath, mode='w', encoding="utf-8") as file:
            json.dump(content, file, indent=4)

        return filepath

    @staticmethod
    def save_html(filename, bs4_content, directory="html", extension=".html", mode='w'):
        filename = filename + extension
        dir = FileManager.get_target_dir(directory)
        filepath = dir / filename.replace("/","_")
        with open(filepath, mode=mode) as file:
            file.write(bs4_content.text)
        return filepath

    @staticmethod
    def get_all_filepaths(folder="json"):
        folder_path = FileManager.get_target_dir(folder)
        filepaths = []
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path, filename)
            if os.path.isfile(full_path):
                filepaths.append(full_path)
        if len(filepaths) == 0:
            os.rmdir(folder_path)
        return filepaths


