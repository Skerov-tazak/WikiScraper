#import pandas
import json
import os
from pathlib import Path

class FileManager:

    @staticmethod
    def private_get_target_dir(directory):
        current = Path.cwd()
        if current.name == "src":
            dir = current.parent / directory
            return dir 
        else:
            dir = Path(directory)
            return dir

    @staticmethod
    def remove_file(filepath):
        if os.path.exists(filepath):
            os.remove(filepath)
        else: 
            raise Exception(f"\nFile {filepath} cannot be deleted - it doesn't exist!\n")

    @staticmethod
    def load_csv_to_pandas(filename, directory="csv"):
        dir = FileManager.private_get_target_dir(directory)
        filepath = dir / filename
 #       return pandas.read_csv(filepath)

    @staticmethod
    def load_json(filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
        return data

    @staticmethod
    def save_csv(filename, table, header=False, directory="csv", extension=".csv"):
        filename = filename + extension
        dir = FileManager.private_get_target_dir(directory)
        dir.mkdir(parents=True, exist_ok=True)
        filepath = dir / filename
   #     data_frame = pandas.read_html(table.prettify(), flavor="bs4")
  #      data_frame[0].to_csv(filepath, header=header)
        return filepath

    @staticmethod
    def save_json(filename, content, directory="json", extension=".json"):
        filename = filename + extension
        dir = FileManager.private_get_target_dir(directory)
        dir.mkdir(parents=True, exist_ok=True)
        filepath = dir / filename
        with open(filepath, 'w', encoding="utf-8") as file:
            json.dump(content, file, indent=4)
        return filepath

    @staticmethod
    def save_html(filename, bs4_content, directory="html", extension=".html"):
        filename = filename + extension
        dir = FileManager.private_get_target_dir(directory)
        dir.mkdir(parents=True, exist_ok=True)
        filepath = dir / filename.replace("/","_")
        with open(filepath, 'w') as file:
            file.write(bs4_content.text)
        return filepath

