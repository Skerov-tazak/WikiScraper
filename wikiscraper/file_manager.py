"""Performs all the necessary file manipulations"""
import pandas
import json
import os
from pathlib import Path

def get_target_dir(directory):
    """Returns the path to the target directory or 
     makes it in parrent of script folder if it does not exist"""
    current = Path(__file__).resolve()
    fold = current.parent.parent / directory
    fold.mkdir(parents=True, exist_ok=True)
    return fold

def remove_file(filepath):
    """Unexists a file"""
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        raise Exception(f"\nFile {filepath} cannot be deleted - it doesn't exist!\n")

def get_file_name(filepath):
    """Returns file name based on path"""
    fileparts = filepath.split("/")
    file = fileparts[len(fileparts) - 1]
    return file

def get_article_name(filepath):
    """Returns file name but without the extension"""
    return get_file_name(filepath).split(".")[0]


def load_csv_to_pandas(filename, directory="csv"):
    """Loads a csv file to a pandas data_frame"""
    fold = get_target_dir(directory)
    filepath = fold / filename
    return pandas.read_csv(filepath)

def load_txt(filename, directory="txt"):
    """Loads a txt file into a string"""
    fold = get_target_dir(directory)
    filepath = fold / filename
    full_list = []
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for l in lines:
            full_list.append(l.split(" ")[-1].replace("\n",""))
    return full_list

def load_json(filename, directory="json"):
    """Loads a json file into a string"""
    fold = get_target_dir(directory)
    filepath = fold / filename
    return json.load(open(filepath, encoding="utf-8"))

def save_csv(filename, data_frame, header=False, directory="csv", extension=".csv", mode="w"):
    """Saves a pandas data_frame to a csv file"""
    filename = filename + extension
    fold = get_target_dir(directory)
    filepath = fold / filename
    data_frame.to_csv(filepath, mode=mode, header=header)
    return filepath

def save_json(filename, content, directory="json", extension=".json", mode="w"):
    """Saves a dictionary to a json file"""
    filename = filename + extension
    fold = get_target_dir(directory)
    filepath = fold / filename

    if mode == "a" and os.path.exists(filepath):
        with open(filepath, mode="r", encoding="utf-8") as file:
            old_content = json.load(file)
            content["total"] += old_content["total"]
            for word in old_content["list"]:
                if word in content["list"]:
                    content["list"][word] += old_content["list"][word]
                else:
                    content["list"].update({word: old_content["list"][word]})

    with open(filepath, mode="w", encoding="utf-8") as file:
        json.dump(content, file, indent=4)

    return filepath

def save_html(filename, bs4_content, directory="html", extension=".html", mode="w"):
    """Saves beautiful soup type object to an html file"""
    filename = filename + extension
    fold = get_target_dir(directory)
    filepath = fold / filename.replace("/","_")
    with open(filepath, mode=mode, encoding="utf-8") as file:
        file.write(bs4_content.text)
    return filepath

def get_all_filepaths(folder="json"):
    """Returns filepaths to all files inside a specified folder"""
    folder_path = get_target_dir(folder)
    filepaths = []
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path):
            filepaths.append(full_path)
    if len(filepaths) == 0:
        os.rmdir(folder_path)
    return filepaths
